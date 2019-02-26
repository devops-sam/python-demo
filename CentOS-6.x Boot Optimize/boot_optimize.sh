#!/bin/bash

## 1.改yum源(阿里或者其他)
mv /etc/yum.repos.d/CentOS-Base.repo{,.bak}
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-6.repo
#yum -y install tree nmap sysstat lrzsz dos2unix telnet  # 安装必要的包

## 2.关闭selinux及iptables
sed -i.ori 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config
setenforce 0
/etc/init.d/iptables stop
chkconf iptables off

## 3.设置运行级别为3(多用户模式)
sed -i.ori 's#id:[0-9]:init#id:3:init#' /etc/inittab

## 4.简化开机启动服务
LANG=en
chkconfig --list|egrep "3:on" |grep -vE "crond|sshd|network|rsyslog|sysstat " |awk '{print "chkconfig "$1" off"}'|bash

## 5.添加sudo用户(可以划分更明细的用户权限)
useradd admin
echo 'admin' |passwd --stdin admin
echo "admin ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

## 6.更改ssh服务远程登录配置
cp /etc/ssh/sshd_config{,.ori}
sed -ri.ori '17aPort 52113\nPermitEmptyPasswords no\nUseDNS no\nGSSAPIAuthentication no\n' /etc/ssh/sshd_config

## 7.更改字符集
cp /etc/sysconfig/i18n{,.ori}
echo 'LANG="zh_CN.UTF-8"'  > /etc/sysconfig/i18n
source /etc/sysconfig/i18n

## 8.服务器时间同步(可选)
#yum install ntpdate -y >/dev/null
#echo '*/5 * * * * /usr/sbin/ntpdate ntp1.aliyun.com >/dev/null 2>&1' >>/var/spool/cron/root

## 9.历史记录数及登录超时设置(可选)
#cat >> /etc/profile.d/his_to.sh << EOF
#export HISTSIZE=5
#export TMOUT=10
#export HISTFILESIZE=10
#EOF

#source /etc/profile.d/his_to.sh

## 10.内核优化
cat >> /etc/sysctl.conf <<EOF
net.ipv4.tcp_fin_timeout = 2  
net.ipv4.tcp_tw_reuse = 1  
net.ipv4.tcp_tw_recycle = 1  
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_keepalive_time = 600
net.ipv4.ip_local_port_range = 4000 65000 
net.ipv4.tcp_max_syn_backlog = 16384
net.ipv4.tcp_max_tw_buckets = 36000
net.ipv4.route.gc_timeout = 100
net.ipv4.tcp_syn_retries = 1
net.ipv4.tcp_synack_retries = 1
net.core.somaxconn = 16384
net.core.netdev_max_backlog = 16384
net.ipv4.tcp_max_orphans = 16384
net.nf_conntrack_max = 25000000
net.netfilter.nf_conntrack_max = 25000000
net.netfilter.nf_conntrack_tcp_timeout_established = 180
net.netfilter.nf_conntrack_tcp_timeout_time_wait = 120
net.netfilter.nf_conntrack_tcp_timeout_close_wait = 60
net.netfilter.nf_conntrack_tcp_timeout_fin_wait = 120
EOF

sysctl -p

## 11.调整linux系统描述符及最大进程数
echo '* - nofile 65535' >>/etc/security/limits.conf
ulimit -SHn 65535
echo '* - nproc 65535' >>/etc/security/limits.conf
ulimit -SHu 65535

#echo 65535 > /proc/sys/kernel/pid_max (貌似大于65535，可以不用调整)
#echo "kernel.pid_max = 65535" >> /etc/sysctl.conf
#sysctl -p

## 12.隐藏linux版本信息
>/etc/issue
>/etc/issue.net

## 13.锁定关键系统文件，防止篡改(可选)
#chattr +i /etc/passwd /etc/shadow /etc/group /etc/gshadow /etc/inittab

## 14.grub加密(可选)
#passwd=`openssl passwd -1 123456 2>/dev/null |tail -1`
#sed -i.ori "/hiddenmenu/apassword --md5 $passwd" /etc/grub.conf

## 15.禁止系统被ping(可选)
#echo “net.ipv4.icmp_echo_ignore_all=1” >> /etc/sysctl.conf
#sysctl -p

## 16.升级具有典型漏掉的软件(可选)
#yum install openssl -y

## 17.定时清理邮件服务临时目录垃圾文件(可选,一般不用,前面的服务都停掉了)
#echo "0 0 * * * find /var/spool/postfix/maildrop/ -type f |xargs rm -f {} " |crontab -
