FROM mysql
EXPOSE 3306

ADD ./my.cnf /etc/mysql/conf.d/my.cnf
ADD ./initdb.d /docker-entrypoint-initdb.d
# ADD ./db /var/lib/mysql

CMD ["mysqld"]