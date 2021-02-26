#!/bin/bash

WAITTIME=30

init()
{
	install -m 0755 ./reboot_test.sh /usr/bin/

	if [[ ! -f /lib/systemd/system/reboot_test.service ]]; then
		cp ./reboot_test.service /lib/systemd/system/reboot_test.service
	fi

	# enable service
	systemctl enable reboot_test

	echo "0" > /opt/rebootno
}

quit()
{
	if [[ -f /usr/bin/reboot_test.sh ]]; then
		rm -f /usr/bin/reboot_test.sh
	fi

	systemctl disable reboot_test

	if [[ -f /lib/systemd/system/reboot_test.service ]]; then
		rm -f /lib/systemd/system/reboot_test.service
	fi

	if [[ -f /opt/rebooted ]]; then
		rm -f /opt/rebooted
	fi

	if [[ -f /opt/rebootmax ]]; then
		rm -f /opt/rebootmax
	fi

	if [[ -f /opt/rebootno ]]; then
		rm -f /opt/rebootno
	fi

	exit 0
}

doreboot()
{
	# write back to file, $1 is the current reboot time
	echo $1 > /opt/rebootno
	sleep ${WAITTIME}
	systemctl reboot
}

rebooted()
{
	touch /opt/rebooted
	echo "Reboot test $1 times successfully." > /opt/reboot_test-result-$(date +%s)

	quit
}

if [[ -f /opt/rebooted ]]; then
	quit
fi

if [[ ! -f /usr/bin/reboot.sh ]]; then
	init
fi

# $1 is the reboot times
if [ "x$1" != "x" ]; then
	if [[ ! -f /opt/rebootmax ]]; then
		echo $1 > /opt/rebootmax
	fi
fi

if [[ ! -f /opt/rebootmax ]]; then
	echo "Failed to init the reboot test."
	echo "First time this script must be used with a max test num."
	echo "Usage: sudo ./reboot.sh 50"

	exit 1
fi

if [[ -f /opt/rebootno ]]; then
	if [[ -f /opt/rebootmax ]]; then
		TestNo=$(expr $(cat /opt/rebootno) + 1)
		TestMax=$(cat /opt/rebootmax)

		if [[ ${TestNo} -le ${TestMax} ]]; then
			doreboot ${TestNo}
		else
			rebooted ${TestMax}
		fi
	fi
	
fi
