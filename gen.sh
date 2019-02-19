# !/bin/sh

# 使用简介
# 功能： 
# 	自动从网络下载 swagger.yaml，并且根据 java-crush-test2.0/template中的模板自动生成代码，默认生成后的一些路径错误问题，使用sed命令批量修改
#
# 配置介绍：
# 	genpath 一般为 swagger-codegen项目所在路径，请到github上 git clone https://github.com/swagger-api/swagger-codegen.git
# 	javapath 为 java-crush-test2.0 的路径，请根据个人实际情况设置
# 	swagger 为 swagger.yaml 的服务器host
#

genpath="."
javapath=~/repos/gitlab/java-crush-test2.0
swagger=http://crush-swagger.c58c7e25a004943cdad05a1bf31f354b7.cn-shenzhen.alicontainer.com

yamls=(tenant sponsor staff venture main otc)

validate=0
echo "Request and Response models need validation?"
select yn in "Yes" "No"; do
        case $yn in
                Yes ) validate=1; break;;
                No ) echo "not release to src"; break;;
        esac
done

function get_yaml()
{
	rm -f $genpath/crush-$1.yaml
	curl $swagger/crush-$1.yaml -o $genpath/crush-$1.yaml
	if [ ! -f $genpath/crush-$1.yaml ]; then
		echo "Download yaml failed!"
		exit -1
	fi
}

function link_template()
{
	unlink $genpath/modules/swagger-codegen/src/main/resources/python
	sync;
	if [ $validate -eq 0 ]; then
		ln -s $javapath/template/no_validate/$1 $genpath/modules/swagger-codegen/src/main/resources/python
	else
		ln -s $javapath/template/validate/$1 $genpath/modules/swagger-codegen/src/main/resources/python
	fi
}

function gen_src()
{
	rm -rf $genpath/$1
	if [ ! -f $genpath/swagger-codegen-cli.jar ]; then
		echo "swagger-codegen-cli.jar is missing"
		exit -1
	fi
	java -jar $genpath/swagger-codegen-cli.jar generate -i $genpath/crush-$1.yaml -l python -t $genpath/modules/swagger-codegen/src/main/resources/python -o $genpath/$1
	sync;
	sed -i "s/&gt;//g" `grep '&gt;' -rl $genpath/$1`
	sed -i "s/null&lt;//g" `grep 'null&lt;' -rl $genpath/$1`
	sed -i "s/swagger_client.models/swagger_client.$1.models/g" `grep swagger_client.models -rl $genpath/$1`
}	

function release_src()
{
	cp $genpath/crush-$1.yaml $javapath/
	if [ -d $javapath/swagger_client/$1 ]; then
		rm -rf $javapath/swagger_client/$1/*
	else
		mkdir -p $javapath/swagger_client/$1
	fi
	cp -rf $genpath/$1/swagger_client/* $javapath/swagger_client/$1/
}

for yaml in ${yamls[*]}
do
	get_yaml $yaml
	rm -rf ./$yaml
	sync;
	link_template $yaml
	gen_src $yaml
done


release=0
echo "Do you wish to release generated src to $javapath ?"
select yn in "Yes" "No"; do
	case $yn in
		Yes ) release=1; break;;
		No ) echo "not release to src"; break;;
	esac
done

if [ $release -eq 1 ]
then
	for yaml in ${yamls[*]}
	do
		release_src $yaml
 	done
fi

sync;
