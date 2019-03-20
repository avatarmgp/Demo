isinuat=$(ifconfig | grep 'inet ' | grep '192.168.19')
myip=$(echo $isinuat | awk '{print $2}' | awk -F: '{print $NF}')
if [[ "$myip" == "" ]]; then
	vpnip=$(ifconfig | grep 'inet ' | grep '10.10')
	if [[ "$vpnip" == "" ]]; then
		vpnip=$(ifconfig | grep 'inet' | grep '192.168.255')
	fi
	if [[ "$vpnip" == "" ]]; then
		echo "can't run ezconsul"
	fi
	myip=$(echo $vpnip | awk '{print $2}' | awk -F: '{print $NF}')
fi
dc=$(hostname | sed 's/\./_/g' | sed 's/-/_/g' | sed 's/__/_/g' | sed 's/MacBook//g')
dc=$(echo zzz_${dc%%_local} | tr '[:upper:]' '[:lower:]')
echo $dc
echo $myip