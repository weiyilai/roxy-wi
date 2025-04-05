import distro

from app.modules.db.db_model import (
	connect, Setting, Role, User, UserGroups, Groups, Services, RoxyTool, Version, GeoipCodes, migrate, mysql_enable, TextField
)
from peewee import IntegerField, SQL


conn = connect()
migrator = connect(get_migrator=1)


def default_values():
	if distro.id() == 'ubuntu':
		apache_dir = 'apache2'
	else:
		apache_dir = 'httpd'
	data_source = [
		{'param': 'time_zone', 'value': 'UTC', 'section': 'main', 'desc': 'Time Zone', 'group_id': '1'},
		{'param': 'license', 'value': '', 'section': 'main', 'desc': 'License key', 'group_id': '1'},
		{'param': 'proxy', 'value': '', 'section': 'main', 'desc': 'IP address and port of the proxy server. Use proto://ip:port', 'group_id': '1'},
		{'param': 'session_ttl', 'value': '5', 'section': 'main', 'desc': 'TTL for a user session (in days)', 'group_id': '1'},
		{'param': 'token_ttl', 'value': '5', 'section': 'main', 'desc': 'TTL for a user token (in days)', 'group_id': '1'},
		{'param': 'tmp_config_path', 'value': '/tmp/', 'section': 'main', 'desc': 'Path to the temporary directory.', 'group_id': '1'},
		{'param': 'cert_path', 'value': '/etc/ssl/certs/', 'section': 'main', 'desc': 'Path to SSL dir.', 'group_id': '1'},
		{'param': 'maxmind_key', 'value': '', 'section': 'main', 'desc': 'License key for downloading GeoIP DB. You can create it on maxmind.com', 'group_id': '1'},
		{'param': 'haproxy_path_logs', 'value': '/var/log/haproxy/', 'section': 'haproxy', 'desc': 'The path for HAProxy logs', 'group_id': '1'},
		{'param': 'syslog_server_enable', 'value': '0', 'section': 'logs', 'desc': 'Enable getting logs from a syslog server', 'group_id': '1'},
		{'param': 'syslog_server', 'value': '', 'section': 'logs', 'desc': 'IP address of the syslog_server', 'group_id': '1'},
		{'param': 'log_time_storage', 'value': '14', 'section': 'logs', 'desc': 'Retention period for user activity logs (in days)', 'group_id': '1'},
		{'param': 'haproxy_stats_user', 'value': 'admin', 'section': 'haproxy', 'desc': 'Username for accessing HAProxy stats page', 'group_id': '1'},
		{'param': 'haproxy_stats_password', 'value': 'password', 'section': 'haproxy', 'desc': 'Password for accessing HAProxy stats page', 'group_id': '1'},
		{'param': 'haproxy_stats_port', 'value': '8085', 'section': 'haproxy', 'desc': 'Port for HAProxy stats page', 'group_id': '1'},
		{'param': 'haproxy_stats_page', 'value': 'stats', 'section': 'haproxy', 'desc': 'URI for HAProxy stats page', 'group_id': '1'},
		{'param': 'haproxy_dir', 'value': '/etc/haproxy', 'section': 'haproxy', 'desc': 'Path to the HAProxy directory', 'group_id': '1'},
		{'param': 'haproxy_config_path', 'value': '/etc/haproxy/haproxy.cfg', 'section': 'haproxy', 'desc': 'Path to the HAProxy configuration file', 'group_id': '1'},
		{'param': 'server_state_file', 'value': '/etc/haproxy/haproxy.state', 'section': 'haproxy', 'desc': 'Path to the HAProxy state file', 'group_id': '1'},
		{'param': 'haproxy_sock', 'value': '/var/run/haproxy.sock', 'section': 'haproxy', 'desc': 'Socket port for HAProxy', 'group_id': '1'},
		{'param': 'haproxy_sock_port', 'value': '1999', 'section': 'haproxy', 'desc': 'HAProxy sock port', 'group_id': '1'},
		{'param': 'haproxy_container_name', 'value': 'haproxy', 'section': 'haproxy', 'desc': 'Docker container name for HAProxy service', 'group_id': '1'},
		{'param': 'apache_log_path', 'value': f'/var/log/{apache_dir}/', 'section': 'logs', 'desc': 'Path to Apache logs. Apache service for Roxy-WI', 'group_id': '1'},
		{'param': 'nginx_path_logs', 'value': '/var/log/nginx/', 'section': 'nginx', 'desc': 'The path for NGINX logs', 'group_id': '1'},
		{'param': 'nginx_stats_user', 'value': 'admin', 'section': 'nginx', 'desc': 'Username for accessing NGINX stats page', 'group_id': '1'},
		{'param': 'nginx_stats_password', 'value': 'password', 'section': 'nginx', 'desc': 'Password for Stats web page NGINX', 'group_id': '1'},
		{'param': 'nginx_stats_port', 'value': '8086', 'section': 'nginx', 'desc': 'Stats port for web page NGINX', 'group_id': '1'},
		{'param': 'nginx_stats_page', 'value': 'stats', 'section': 'nginx', 'desc': 'URI Stats for web page NGINX', 'group_id': '1'},
		{'param': 'nginx_dir', 'value': '/etc/nginx/', 'section': 'nginx', 'desc': 'Path to the NGINX directory with config files', 'group_id': '1'},
		{'param': 'nginx_config_path', 'value': '/etc/nginx/nginx.conf', 'section': 'nginx', 'desc': 'Path to the main NGINX configuration file', 'group_id': '1'},
		{'param': 'nginx_container_name', 'value': 'nginx', 'section': 'nginx', 'desc': 'Docker container name for NGINX service', 'group_id': '1'},
		{'param': 'ldap_enable', 'value': '0', 'section': 'ldap', 'desc': 'Enable LDAP', 'group_id': '1'},
		{'param': 'ldap_server', 'value': '', 'section': 'ldap', 'desc': 'IP address of the LDAP server', 'group_id': '1'},
		{'param': 'ldap_port', 'value': '389', 'section': 'ldap', 'desc': 'LDAP port (port 389 or 636 is used by default)', 'group_id': '1'},
		{'param': 'ldap_user', 'value': '', 'section': 'ldap', 'desc': 'LDAP username. Format: user@domain.com', 'group_id': '1'},
		{'param': 'ldap_password', 'value': '', 'section': 'ldap', 'desc': 'LDAP password', 'group_id': '1'},
		{'param': 'ldap_base', 'value': '', 'section': 'ldap', 'desc': 'Base domain. Example: dc=domain, dc=com', 'group_id': '1'},
		{'param': 'ldap_domain', 'value': '', 'section': 'ldap', 'desc': 'LDAP domain for logging in', 'group_id': '1'},
		{'param': 'ldap_class_search', 'value': 'user', 'section': 'ldap', 'desc': 'Class for searching the user', 'group_id': '1'},
		{'param': 'ldap_user_attribute', 'value': 'userPrincipalName', 'section': 'ldap', 'desc': 'Attribute to search users by', 'group_id': '1'},
		{'param': 'ldap_search_field', 'value': 'mail', 'section': 'ldap', 'desc': 'User\'s email address', 'group_id': '1'},
		{'param': 'ldap_type', 'value': '0', 'section': 'ldap', 'desc': 'Use LDAPS', 'group_id': '1'},
		{'param': 'port_scan_interval', 'value': '5', 'section': 'monitoring', 'desc': 'Check interval for Port scanner (in minutes)', 'group_id': '1'},
		{'param': 'portscanner_keep_history_range', 'value': '14', 'section': 'monitoring', 'desc': 'Retention period for Port scanner history', 'group_id': '1'},
		{'param': 'smon_keep_history_range', 'value': '14', 'section': 'smon', 'desc': 'Retention period for SMON history', 'group_id': '1'},
		{'param': 'checker_keep_history_range', 'value': '14', 'section': 'monitoring', 'desc': 'Retention period for Checker history', 'group_id': '1'},
		{'param': 'action_keep_history_range', 'value': '30', 'section': 'monitoring', 'desc': 'Retention period for Action history', 'group_id': '1'},
		{'param': 'checker_maxconn_threshold', 'value': '90', 'section': 'monitoring', 'desc': 'Threshold value for alerting, in %', 'group_id': '1'},
		{'param': 'checker_check_interval', 'value': '1', 'section': 'monitoring', 'desc': 'Check interval for Checker (in minutes)', 'group_id': '1'},
		{'param': 'smon_ssl_expire_warning_alert', 'value': '14', 'section': 'smon', 'desc': 'Warning alert about a SSL certificate expiration (in days)', 'group_id': '1'},
		{'param': 'smon_ssl_expire_critical_alert', 'value': '7', 'section': 'smon', 'desc': 'Critical alert about a SSL certificate expiration (in days)', 'group_id': '1'},
		{'param': 'master_ip', 'value': '', 'section': 'smon', 'desc': '', 'group_id': '1'},
		{'param': 'master_port', 'value': '5100', 'section': 'smon', 'desc': '', 'group_id': '1'},
		{'param': 'agent_port', 'value': '5101', 'section': 'smon', 'desc': '', 'group_id': '1'},
		{'param': 'rabbitmq_host', 'value': '127.0.0.1', 'section': 'rabbitmq', 'desc': 'RabbitMQ-server host', 'group_id': '1'},
		{'param': 'rabbitmq_port', 'value': '5672', 'section': 'rabbitmq', 'desc': 'RabbitMQ-server port', 'group_id': '1'},
		{'param': 'rabbitmq_port', 'value': '5672', 'section': 'rabbitmq', 'desc': 'RabbitMQ-server port', 'group_id': '1'},
		{'param': 'rabbitmq_vhost', 'value': '/', 'section': 'rabbitmq', 'desc': 'RabbitMQ-server vhost', 'group_id': '1'},
		{'param': 'rabbitmq_queue', 'value': 'roxy-wi', 'section': 'rabbitmq', 'desc': 'RabbitMQ-server queue', 'group_id': '1'},
		{'param': 'rabbitmq_user', 'value': 'roxy-wi', 'section': 'rabbitmq', 'desc': 'RabbitMQ-server user', 'group_id': '1'},
		{'param': 'rabbitmq_password', 'value': 'roxy-wi123', 'section': 'rabbitmq', 'desc': 'RabbitMQ-server user password', 'group_id': '1'},
		{'param': 'apache_path_logs', 'value': '/var/log/httpd/', 'section': 'apache', 'desc': 'The path for Apache logs', 'group_id': '1'},
		{'param': 'apache_stats_user', 'value': 'admin', 'section': 'apache', 'desc': 'Username for accessing Apache stats page', 'group_id': '1'},
		{'param': 'apache_stats_password', 'value': 'password', 'section': 'apache', 'desc': 'Password for Apache stats webpage', 'group_id': '1'},
		{'param': 'apache_stats_port', 'value': '8087', 'section': 'apache', 'desc': 'Stats port for webpage Apache', 'group_id': '1'},
		{'param': 'apache_stats_page', 'value': 'stats', 'section': 'apache', 'desc': 'URI Stats for webpage Apache', 'group_id': '1'},
		{'param': 'apache_dir', 'value': '/etc/httpd/', 'section': 'apache', 'desc': 'Path to the Apache directory with config files', 'group_id': '1'},
		{'param': 'apache_config_path', 'value': '/etc/httpd/conf/httpd.conf', 'section': 'apache', 'desc': 'Path to the main Apache configuration file', 'group_id': '1'},
		{'param': 'apache_container_name', 'value': 'apache', 'section': 'apache', 'desc': 'Docker container name for Apache service', 'group_id': '1'},
		{'param': 'keepalived_config_path', 'value': '/etc/keepalived/keepalived.conf', 'section': 'keepalived', 'desc': 'Path to the main Keepalived configuration file', 'group_id': '1'},
		{'param': 'keepalived_path_logs', 'value': '/var/log/keepalived/', 'section': 'keepalived', 'desc': 'The path for Keepalived logs', 'group_id': '1'},
		{'param': 'mail_ssl', 'value': '0', 'section': 'mail', 'desc': 'Enable TLS', 'group_id': '1'},
		{'param': 'mail_from', 'value': '', 'section': 'mail', 'desc': 'Address of sender', 'group_id': '1'},
		{'param': 'mail_smtp_host', 'value': '', 'section': 'mail', 'desc': 'SMTP server address', 'group_id': '1'},
		{'param': 'mail_smtp_port', 'value': '25', 'section': 'mail', 'desc': 'SMTP server port', 'group_id': '1'},
		{'param': 'mail_smtp_user', 'value': '', 'section': 'mail', 'desc': 'User for auth', 'group_id': '1'},
		{'param': 'mail_smtp_password', 'value': '', 'section': 'mail', 'desc': 'Password for auth', 'group_id': '1'},
	]
	try:
		Setting.insert_many(data_source).on_conflict_ignore().execute()
	except Exception as e:
		print(str(e))

	data_source = [
		{'username': 'admin', 'email': 'admin@localhost', 'password': '21232f297a57a5a743894a0e4a801fc3', 'role_id': '1', 'group_id': '1'},
		{'username': 'editor', 'email': 'editor@localhost', 'password': '5aee9dbd2a188839105073571bee1b1f', 'role_id': '2', 'group_id': '1'},
		{'username': 'guest', 'email': 'guest@localhost', 'password': '084e0343a0486ff05530df6c705c8bb4', 'role_id': '4', 'group_id': '1'}
	]

	try:
		if Role.get(Role.name == 'superAdmin').role_id == 1:
			create_users = False
		else:
			create_users = True
	except Exception:
		create_users = True

	try:
		if create_users:
			User.insert_many(data_source).on_conflict_ignore().execute()
	except Exception as e:
		print(str(e))

	data_source = [
		{'user_id': '1', 'user_group_id': '1', 'user_role_id': '1'},
		{'user_id': '2', 'user_group_id': '1', 'user_role_id': '2'},
		{'user_id': '3', 'user_group_id': '1', 'user_role_id': '4'}
	]

	try:
		if create_users:
			UserGroups.insert_many(data_source).on_conflict_ignore().execute()
	except Exception as e:
		print(str(e))

	data_source = [
		{'name': 'superAdmin',
		 'description': 'Has the highest level of administrative permissions and controls the actions of all other users'},
		{'name': 'admin', 'description': 'Has admin access to its groups'},
		{'name': 'user', 'description': 'Has the same rights as the admin but has no access to the Admin area'},
		{'name': 'guest', 'description': 'Read-only access'}
	]

	try:
		Role.insert_many(data_source).on_conflict_ignore().execute()
	except Exception as e:
		print(str(e))

	try:
		Groups.insert(name='Default', description='All servers are included in this group by default', id=1).on_conflict_ignore().execute()
	except Exception as e:
		print(str(e))

	data_source = [
		{'service_id': 1, 'service': 'HAProxy', 'slug': 'haproxy'},
		{'service_id': 2, 'service': 'NGINX', 'slug': 'nginx'},
		{'service_id': 3, 'service': 'Keepalived', 'slug': 'keepalived'},
		{'service_id': 4, 'service': 'Apache', 'slug': 'apache'},
		{'service_id': 5, 'service': 'HA cluster', 'slug': 'cluster'},
		{'service_id': 6, 'service': 'UDP listener', 'slug': 'udp'},
	]

	try:
		Services.insert_many(data_source).on_conflict_ignore().execute()
	except Exception:
		Services.drop_table()
		Services.create_table()
		try:
			Services.insert_many(data_source).on_conflict_ignore().execute()
		except Exception as e:
			print(str(e))

	data_source = [
		{'code': 'RW', 'name': 'Rwanda'},
		{'code': 'SO', 'name': 'Somalia'},
		{'code': 'YE', 'name': 'Yemen'},
		{'code': 'IQ', 'name': 'Iraq'},
		{'code': 'SA', 'name': 'Saudi Arabia'},
		{'code': 'IR', 'name': 'Iran'},
		{'code': 'CY', 'name': 'Cyprus'},
		{'code': 'TZ', 'name': 'Tanzania'},
		{'code': 'SY', 'name': 'Syria'},
		{'code': 'AM', 'name': 'Armenia'},
		{'code': 'KE', 'name': 'Kenya'},
		{'code': 'CD', 'name': 'DR Congo'},
		{'code': 'DJ', 'name': 'Djibouti'},
		{'code': 'UG', 'name': 'Uganda'},
		{'code': 'CF', 'name': 'Central African Republic'},
		{'code': 'SC', 'name': 'Seychelles'},
		{'code': 'JO', 'name': 'Hashemite Kingdom of Jordan'},
		{'code': 'LB', 'name': 'Lebanon'},
		{'code': 'KW', 'name': 'Kuwait'},
		{'code': 'OM', 'name': 'Oman'},
		{'code': 'QA', 'name': 'Qatar'},
		{'code': 'BH', 'name': 'Bahrain'},
		{'code': 'AE', 'name': 'United Arab Emirates'},
		{'code': 'IL', 'name': 'Israel'},
		{'code': 'TR', 'name': 'Turkey'},
		{'code': 'ET', 'name': 'Ethiopia'},
		{'code': 'ER', 'name': 'Eritrea'},
		{'code': 'EG', 'name': 'Egypt'},
		{'code': 'SD', 'name': 'Sudan'},
		{'code': 'GR', 'name': 'Greece'},
		{'code': 'BI', 'name': 'Burundi'},
		{'code': 'EE', 'name': 'Estonia'},
		{'code': 'LV', 'name': 'Latvia'},
		{'code': 'AZ', 'name': 'Azerbaijan'},
		{'code': 'LT', 'name': 'Republic of Lithuania'},
		{'code': 'SJ', 'name': 'Svalbard and Jan Mayen'},
		{'code': 'GE', 'name': 'Georgia'},
		{'code': 'MD', 'name': 'Republic of Moldova'},
		{'code': 'BY', 'name': 'Belarus'},
		{'code': 'FI', 'name': 'Finland'},
		{'code': 'AX', 'name': 'Åland'},
		{'code': 'UA', 'name': 'Ukraine'},
		{'code': 'MK', 'name': 'North Macedonia'},
		{'code': 'HU', 'name': 'Hungary'},
		{'code': 'BG', 'name': 'Bulgaria'},
		{'code': 'AL', 'name': 'Albania'},
		{'code': 'PL', 'name': 'Poland'},
		{'code': 'RO', 'name': 'Romania'},
		{'code': 'XK', 'name': 'Kosovo'},
		{'code': 'ZW', 'name': 'Zimbabwe'},
		{'code': 'ZM', 'name': 'Zambia'},
		{'code': 'KM', 'name': 'Comoros'},
		{'code': 'MW', 'name': 'Malawi'},
		{'code': 'LS', 'name': 'Lesotho'},
		{'code': 'BW', 'name': 'Botswana'},
		{'code': 'MU', 'name': 'Mauritius'},
		{'code': 'SZ', 'name': 'Eswatini'},
		{'code': 'RE', 'name': 'Réunion'},
		{'code': 'ZA', 'name': 'South Africa'},
		{'code': 'YT', 'name': 'Mayotte'},
		{'code': 'MZ', 'name': 'Mozambique'},
		{'code': 'MG', 'name': 'Madagascar'},
		{'code': 'AF', 'name': 'Afghanistan'},
		{'code': 'PK', 'name': 'Pakistan'},
		{'code': 'BD', 'name': 'Bangladesh'},
		{'code': 'TM', 'name': 'Turkmenistan'},
		{'code': 'TJ', 'name': 'Tajikistan'},
		{'code': 'LK', 'name': 'Sri Lanka'},
		{'code': 'BT', 'name': 'Bhutan'},
		{'code': 'IN', 'name': 'India'},
		{'code': 'MV', 'name': 'Maldives'},
		{'code': 'IO', 'name': 'British Indian Ocean Territory'},
		{'code': 'NP', 'name': 'Nepal'},
		{'code': 'MM', 'name': 'Myanmar'},
		{'code': 'UZ', 'name': 'Uzbekistan'},
		{'code': 'KZ', 'name': 'Kazakhstan'},
		{'code': 'KG', 'name': 'Kyrgyzstan'},
		{'code': 'TF', 'name': 'French Southern Territories'},
		{'code': 'HM', 'name': 'Heard Island and McDonald Islands'},
		{'code': 'CC', 'name': 'Cocos [Keeling] Islands'},
		{'code': 'PW', 'name': 'Palau'},
		{'code': 'VN', 'name': 'Vietnam'},
		{'code': 'TH', 'name': 'Thailand'},
		{'code': 'ID', 'name': 'Indonesia'},
		{'code': 'LA', 'name': 'Laos'},
		{'code': 'TW', 'name': 'Taiwan'},
		{'code': 'PH', 'name': 'Philippines'},
		{'code': 'MY', 'name': 'Malaysia'},
		{'code': 'CN', 'name': 'China'},
		{'code': 'HK', 'name': 'Hong Kong'},
		{'code': 'BN', 'name': 'Brunei'},
		{'code': 'MO', 'name': 'Macao'},
		{'code': 'KH', 'name': 'Cambodia'},
		{'code': 'KR', 'name': 'South Korea'},
		{'code': 'JP', 'name': 'Japan'},
		{'code': 'KP', 'name': 'North Korea'},
		{'code': 'SG', 'name': 'Singapore'},
		{'code': 'CK', 'name': 'Cook Islands'},
		{'code': 'TL', 'name': 'East Timor'},
		{'code': 'RU', 'name': 'Russia'},
		{'code': 'MN', 'name': 'Mongolia'},
		{'code': 'AU', 'name': 'Australia'},
		{'code': 'CX', 'name': 'Christmas Island'},
		{'code': 'MH', 'name': 'Marshall Islands'},
		{'code': 'FM', 'name': 'Federated States of Micronesia'},
		{'code': 'PG', 'name': 'Papua New Guinea'},
		{'code': 'SB', 'name': 'Solomon Islands'},
		{'code': 'TV', 'name': 'Tuvalu'},
		{'code': 'NR', 'name': 'Nauru'},
		{'code': 'VU', 'name': 'Vanuatu'},
		{'code': 'NC', 'name': 'New Caledonia'},
		{'code': 'NF', 'name': 'Norfolk Island'},
		{'code': 'NZ', 'name': 'New Zealand'},
		{'code': 'FJ', 'name': 'Fiji'},
		{'code': 'LY', 'name': 'Libya'},
		{'code': 'CM', 'name': 'Cameroon'},
		{'code': 'SN', 'name': 'Senegal'},
		{'code': 'CG', 'name': 'Congo Republic'},
		{'code': 'PT', 'name': 'Portugal'},
		{'code': 'LR', 'name': 'Liberia'},
		{'code': 'CI', 'name': 'Ivory Coast'},
		{'code': 'GH', 'name': 'Ghana'},
		{'code': 'GQ', 'name': 'Equatorial Guinea'},
		{'code': 'NG', 'name': 'Nigeria'},
		{'code': 'BF', 'name': 'Burkina Faso'},
		{'code': 'TG', 'name': 'Togo'},
		{'code': 'GW', 'name': 'Guinea-Bissau'},
		{'code': 'MR', 'name': 'Mauritania'},
		{'code': 'BJ', 'name': 'Benin'},
		{'code': 'GA', 'name': 'Gabon'},
		{'code': 'SL', 'name': 'Sierra Leone'},
		{'code': 'ST', 'name': 'São Tomé and Príncipe'},
		{'code': 'GI', 'name': 'Gibraltar'},
		{'code': 'GM', 'name': 'Gambia'},
		{'code': 'GN', 'name': 'Guinea'},
		{'code': 'TD', 'name': 'Chad'},
		{'code': 'NE', 'name': 'Niger'},
		{'code': 'ML', 'name': 'Mali'},
		{'code': 'EH', 'name': 'Western Sahara'},
		{'code': 'TN', 'name': 'Tunisia'},
		{'code': 'ES', 'name': 'Spain'},
		{'code': 'MA', 'name': 'Morocco'},
		{'code': 'MT', 'name': 'Malta'},
		{'code': 'DZ', 'name': 'Algeria'},
		{'code': 'FO', 'name': 'Faroe Islands'},
		{'code': 'DK', 'name': 'Denmark'},
		{'code': 'IS', 'name': 'Iceland'},
		{'code': 'GB', 'name': 'United Kingdom'},
		{'code': 'CH', 'name': 'Switzerland'},
		{'code': 'SE', 'name': 'Sweden'},
		{'code': 'NL', 'name': 'Netherlands'},
		{'code': 'AT', 'name': 'Austria'},
		{'code': 'BE', 'name': 'Belgium'},
		{'code': 'DE', 'name': 'Germany'},
		{'code': 'LU', 'name': 'Luxembourg'},
		{'code': 'IE', 'name': 'Ireland'},
		{'code': 'MC', 'name': 'Monaco'},
		{'code': 'FR', 'name': 'France'},
		{'code': 'AD', 'name': 'Andorra'},
		{'code': 'LI', 'name': 'Liechtenstein'},
		{'code': 'JE', 'name': 'Jersey'},
		{'code': 'IM', 'name': 'Isle of Man'},
		{'code': 'GG', 'name': 'Guernsey'},
		{'code': 'SK', 'name': 'Slovakia'},
		{'code': 'CZ', 'name': 'Czechia'},
		{'code': 'NO', 'name': 'Norway'},
		{'code': 'VA', 'name': 'Vatican City'},
		{'code': 'SM', 'name': 'San Marino'},
		{'code': 'IT', 'name': 'Italy'},
		{'code': 'SI', 'name': 'Slovenia'},
		{'code': 'ME', 'name': 'Montenegro'},
		{'code': 'HR', 'name': 'Croatia'},
		{'code': 'BA', 'name': 'Bosnia and Herzegovina'},
		{'code': 'AO', 'name': 'Angola'},
		{'code': 'NA', 'name': 'Namibia'},
		{'code': 'SH', 'name': 'Saint Helena'},
		{'code': 'BV', 'name': 'Bouvet Island'},
		{'code': 'BB', 'name': 'Barbados'},
		{'code': 'CV', 'name': 'Cabo Verde'},
		{'code': 'GY', 'name': 'Guyana'},
		{'code': 'GF', 'name': 'French Guiana'},
		{'code': 'SR', 'name': 'Suriname'},
		{'code': 'PM', 'name': 'Saint Pierre and Miquelon'},
		{'code': 'GL', 'name': 'Greenland'},
		{'code': 'PY', 'name': 'Paraguay'},
		{'code': 'UY', 'name': 'Uruguay'},
		{'code': 'BR', 'name': 'Brazil'},
		{'code': 'FK', 'name': 'Falkland Islands'},
		{'code': 'GS', 'name': 'South Georgia and the South Sandwich Islands'},
		{'code': 'JM', 'name': 'Jamaica'},
		{'code': 'DO', 'name': 'Dominican Republic'},
		{'code': 'CU', 'name': 'Cuba'},
		{'code': 'MQ', 'name': 'Martinique'},
		{'code': 'BS', 'name': 'Bahamas'},
		{'code': 'BM', 'name': 'Bermuda'},
		{'code': 'AI', 'name': 'Anguilla'},
		{'code': 'TT', 'name': 'Trinidad and Tobago'},
		{'code': 'KN', 'name': 'St Kitts and Nevis'},
		{'code': 'DM', 'name': 'Dominica'},
		{'code': 'AG', 'name': 'Antigua and Barbuda'},
		{'code': 'LC', 'name': 'Saint Lucia'},
		{'code': 'TC', 'name': 'Turks and Caicos Islands'},
		{'code': 'AW', 'name': 'Aruba'},
		{'code': 'VG', 'name': 'British Virgin Islands'},
		{'code': 'VC', 'name': 'Saint Vincent and the Grenadines'},
		{'code': 'MS', 'name': 'Montserrat'},
		{'code': 'MF', 'name': 'Saint Martin'},
		{'code': 'BL', 'name': 'Saint Barthélemy'},
		{'code': 'GP', 'name': 'Guadeloupe'},
		{'code': 'GD', 'name': 'Grenada'},
		{'code': 'KY', 'name': 'Cayman Islands'},
		{'code': 'BZ', 'name': 'Belize'},
		{'code': 'SV', 'name': 'El Salvador'},
		{'code': 'GT', 'name': 'Guatemala'},
		{'code': 'HN', 'name': 'Honduras'},
		{'code': 'NI', 'name': 'Nicaragua'},
		{'code': 'CR', 'name': 'Costa Rica'},
		{'code': 'VE', 'name': 'Venezuela'},
		{'code': 'EC', 'name': 'Ecuador'},
		{'code': 'CO', 'name': 'Colombia'},
		{'code': 'PA', 'name': 'Panama'},
		{'code': 'HT', 'name': 'Haiti'},
		{'code': 'AR', 'name': 'Argentina'},
		{'code': 'CL', 'name': 'Chile'},
		{'code': 'BO', 'name': 'Bolivia'},
		{'code': 'PE', 'name': 'Peru'},
		{'code': 'MX', 'name': 'Mexico'},
		{'code': 'PF', 'name': 'French Polynesia'},
		{'code': 'PN', 'name': 'Pitcairn Islands'},
		{'code': 'KI', 'name': 'Kiribati'},
		{'code': 'TK', 'name': 'Tokelau'},
		{'code': 'TO', 'name': 'Tonga'},
		{'code': 'WF', 'name': 'Wallis and Futuna'},
		{'code': 'WS', 'name': 'Samoa'},
		{'code': 'NU', 'name': 'Niue'},
		{'code': 'MP', 'name': 'Northern Mariana Islands'},
		{'code': 'GU', 'name': 'Guam'},
		{'code': 'PR', 'name': 'Puerto Rico'},
		{'code': 'VI', 'name': 'U.S. Virgin Islands'},
		{'code': 'UM', 'name': 'U.S. Minor Outlying Islands'},
		{'code': 'AS', 'name': 'American Samoa'},
		{'code': 'CA', 'name': 'Canada'},
		{'code': 'US', 'name': 'United States'},
		{'code': 'PS', 'name': 'Palestine'},
		{'code': 'RS', 'name': 'Serbia'},
		{'code': 'AQ', 'name': 'Antarctica'},
		{'code': 'SX', 'name': 'Sint Maarten'},
		{'code': 'CW', 'name': 'Curaçao'},
		{'code': 'BQ', 'name': 'Bonaire'},
		{'code': 'SS', 'name': 'South Sudan'}
	]

	try:
		GeoipCodes.insert_many(data_source).on_conflict_ignore().execute()
	except Exception as e:
		print(str(e))

	data_source = [
		{'name': 'roxy-wi-metrics', 'current_version': '1.0', 'new_version': '0', 'is_roxy': 1, 'desc': ''},
		{'name': 'roxy-wi-checker', 'current_version': '1.0', 'new_version': '0', 'is_roxy': 1, 'desc': ''},
		{'name': 'roxy-wi-keep_alive', 'current_version': '1.0', 'new_version': '0', 'is_roxy': 1, 'desc': ''},
		{'name': 'roxy-wi-portscanner', 'current_version': '1.0', 'new_version': '0', 'is_roxy': 1, 'desc': ''},
		{'name': 'roxy-wi-socket', 'current_version': '1.0', 'new_version': '0', 'is_roxy': 1, 'desc': ''},
		{'name': 'roxy-wi-prometheus-exporter', 'current_version': '1.0', 'new_version': '0', 'is_roxy': 1, 'desc': ''},
		{'name': 'roxy-wi-smon', 'current_version': '1.0', 'new_version': '0', 'is_roxy': 1, 'desc': ''},
		{'name': 'fail2ban', 'current_version': '1.0', 'new_version': '1.0', 'is_roxy': 0, 'desc': 'Fail2ban service'},
		{'name': 'rabbitmq-server', 'current_version': '1.0', 'new_version': '1.0', 'is_roxy': 0, 'desc': 'Rabbitmq service'},
	]

	try:
		RoxyTool.insert_many(data_source).on_conflict_ignore().execute()
	except Exception as e:
		print(str(e))


# Needs for insert version in first time
def update_db_v_3_4_5_22():
	try:
		Version.insert(version='3.4.5.2').execute()
	except Exception as e:
		print('Cannot insert version %s' % e)


# Needs for updating user_group. Do not delete
def update_db_v_4_3_0():
	try:
		UserGroups.insert_from(
			User.select(User.user_id, User.group_id), fields=[UserGroups.user_id, UserGroups.user_group_id]
		).on_conflict_ignore().execute()
	except Exception as e:
		if e.args[0] == 'duplicate column name: haproxy' or str(e) == '(1060, "Duplicate column name \'haproxy\'")':
			print('Updating... go to version 4.3.1')
		else:
			print("An error occurred:", e)


def update_db_v_7_2_0():
	try:
		if mysql_enable:
			migrate(
				migrator.add_column('smon_ping_check', 'interval', IntegerField(default=120)),
				migrator.add_column('smon_http_check', 'interval', IntegerField(default=120)),
				migrator.add_column('smon_tcp_check', 'interval', IntegerField(default=120)),
				migrator.add_column('smon_dns_check', 'interval', IntegerField(default=120)),
				migrator.add_column('smon_ping_check', 'agent_id', IntegerField(default=1)),
				migrator.add_column('smon_http_check', 'agent_id', IntegerField(default=1)),
				migrator.add_column('smon_tcp_check', 'agent_id', IntegerField(default=1)),
				migrator.add_column('smon_dns_check', 'agent_id', IntegerField(default=1))
			)
		else:
			migrate(
				migrator.add_column('smon_ping_check', 'interval', IntegerField(constraints=[SQL('DEFAULT 120')])),
				migrator.add_column('smon_http_check', 'interval', IntegerField(constraints=[SQL('DEFAULT 120')])),
				migrator.add_column('smon_tcp_check', 'interval', IntegerField(constraints=[SQL('DEFAULT 120')])),
				migrator.add_column('smon_dns_check', 'interval', IntegerField(constraints=[SQL('DEFAULT 120')])),
				migrator.add_column('smon_ping_check', 'agent_id', IntegerField(constraints=[SQL('DEFAULT 1')])),
				migrator.add_column('smon_http_check', 'agent_id', IntegerField(constraints=[SQL('DEFAULT 1')])),
				migrator.add_column('smon_tcp_check', 'agent_id', IntegerField(constraints=[SQL('DEFAULT 1')])),
				migrator.add_column('smon_dns_check', 'agent_id', IntegerField(constraints=[SQL('DEFAULT 1')]))
			)
	except Exception as e:
		if e.args[0] == 'duplicate column name: agent_id' or str(e) == '(1060, "Duplicate column name \'agent_id\'")':
			print('Updating... DB has been updated to version 7.2.0')
		elif e.args[0] == 'duplicate column name: interval' or str(e) == '(1060, "Duplicate column name \'interval\'")':
			print('Updating... DB has been updated to version 7.2.0')
		else:
			print("An error occurred:", e)


def update_db_v_7_2_0_1():
	try:
		Setting.delete().where(Setting.param == 'smon_check_interval').execute()
		Setting.delete().where((Setting.param == 'smon_keep_history_range') & (Setting.section == 'monitoring')).execute()
		Setting.delete().where((Setting.param == 'smon_ssl_expire_warning_alert') & (Setting.section == 'monitoring')).execute()
		Setting.delete().where((Setting.param == 'smon_ssl_expire_critical_alert') & (Setting.section == 'monitoring')).execute()
	except Exception as e:
		print("An error occurred:", e)
	else:
		print("Updating... DB has been updated to version 7.2.0-1")


def update_db_v_7_2_3():
	try:
		if mysql_enable:
			migrate(
				migrator.add_column('checker_setting', 'mm_id', IntegerField(default=0)),
				migrator.add_column('smon', 'mm_channel_id', IntegerField(default=0)),
			)
		else:
			migrate(
				migrator.add_column('checker_setting', 'mm_id', IntegerField(constraints=[SQL('DEFAULT 0')])),
				migrator.add_column('smon', 'mm_channel_id', IntegerField(constraints=[SQL('DEFAULT 0')])),
			)
	except Exception as e:
		if e.args[0] == 'duplicate column name: mm_id' or str(e) == '(1060, "Duplicate column name \'mm_id\'")':
			print('Updating... DB has been updated to version 7.2.3')
		else:
			print("An error occurred:", e)


def update_db_v_7_3_1():
	try:
		if mysql_enable:
			migrate(
				migrator.add_column('ha_cluster_vips', 'use_src', IntegerField(default=0)),
			)
		else:
			migrate(
				migrator.add_column('ha_cluster_vips', 'use_src', IntegerField(constraints=[SQL('DEFAULT 0')])),
			)
	except Exception as e:
		if e.args[0] == 'duplicate column name: use_src' or str(e) == '(1060, "Duplicate column name \'use_src\'")':
			print('Updating... DB has been updated to version 7.3.1')
		else:
			print("An error occurred:", e)


def update_db_v_7_4():
	try:
		migrate(
			migrator.rename_column('backups', 'cred', 'cred_id'),
			migrator.rename_column('backups', 'backup_type', 'type'),
		)
	except Exception as e:
		if e.args[0] == 'no such column: "cred"' or str(e) == '(1060, no such column: "cred")':
			print("Updating... DB has been updated to version 7.4")
		elif e.args[0] == "'bool' object has no attribute 'sql'":
			print("Updating... DB has been updated to version 7.4")
		else:
			print("An error occurred:", e)


def update_db_v_8():
	try:
		migrate(
			migrator.rename_column('telegram', 'groups', 'group_id'),
			migrator.rename_column('slack', 'groups', 'group_id'),
			migrator.rename_column('mattermost', 'groups', 'group_id'),
			migrator.rename_column('pd', 'groups', 'group_id'),
			migrator.rename_column('servers', 'groups', 'group_id'),
			migrator.rename_column('udp_balancers', 'desc', 'description'),
			migrator.rename_column('ha_clusters', 'desc', 'description'),
			migrator.rename_column('cred', 'enable', 'key_enabled'),
			migrator.rename_column('cred', 'groups', 'group_id'),
			migrator.rename_column('servers', 'desc', 'description'),
			migrator.rename_column('servers', 'active', 'haproxy_active'),
			migrator.rename_column('servers', 'metrics', 'haproxy_metrics'),
			migrator.rename_column('servers', 'alert', 'haproxy_alert'),
			migrator.rename_column('servers', 'cred', 'cred_id'),
			migrator.rename_column('servers', 'enable', 'enabled'),
			migrator.rename_column('servers', 'groups', 'group_id'),
			migrator.rename_column('user', 'activeuser', 'enabled'),
			migrator.rename_column('user', 'groups', 'group_id'),
			migrator.rename_column('user', 'role', 'role_id'),
		)
	except Exception as e:
		if e.args[0] == 'no such column: "groups"' or str(e) == '(1060, no such column: "groups")':
			print("Updating... DB has been updated to version 8")
		elif e.args[0] == "'bool' object has no attribute 'sql'":
			print("Updating... DB has been updated to version 8")
		else:
			print("An error occurred:", e)


def update_db_v_8_0_2():
	try:
		if mysql_enable:
			migrate(
				migrator.add_column('cred', 'shared', IntegerField(default=0)),
			)
		else:
			migrate(
				migrator.add_column('cred', 'shared', IntegerField(constraints=[SQL('DEFAULT 0')])),
			)
	except Exception as e:
		if e.args[0] == 'duplicate column name: shared' or str(e) == '(1060, "Duplicate column name \'shared\'")':
			print('Updating... DB has been updated to version 8.0.2')
		else:
			print("An error occurred:", e)


def update_db_v_8_0_2_1():
	try:
		RoxyTool.delete().where(RoxyTool.name == 'prometheus').execute()
		RoxyTool.delete().where(RoxyTool.name == 'grafana-server').execute()
	except Exception as e:
		print("An error occurred:", e)
	else:
		print("Updating... DB has been updated to version 8.0.2-1")


def update_db_v_8_1():
	try:
		migrate(
			migrator.rename_column('backups', 'server', 'server_id')
		)
	except Exception as e:
		if e.args[0] == 'no such column: "server"' or str(e) == '(1060, no such column: "server")':
			print("Updating... DB has been updated to version 8.2")
		elif e.args[0] == "'bool' object has no attribute 'sql'":
			print("Updating... DB has been updated to version 8.2")
		else:
			print("An error occurred:", e)


def update_db_v_8_1_0_1():
	try:
		migrate(
			migrator.rename_column('s3_backups', 'server', 'server_id')
		)
	except Exception as e:
		if e.args[0] == 'no such column: "server"' or str(e) == '(1060, no such column: "server")':
			print("Updating... DB has been updated to version 8.2")
		elif e.args[0] == "'bool' object has no attribute 'sql'":
			print("Updating... DB has been updated to version 8.2")
		else:
			print("An error occurred:", e)


def update_db_v_8_1_0_2():
	try:
		migrate(
			migrator.rename_column('backups', 'rhost', 'rserver')
		)
	except Exception as e:
		if e.args[0] == 'no such column: "rhost"' or str(e) == '(1060, no such column: "rhost")':
			print("Updating... DB has been updated to version 8.2")
		elif e.args[0] == "'bool' object has no attribute 'sql'":
			print("Updating... DB has been updated to version 8.2")
		else:
			print("An error occurred:", e)


def update_db_v_8_1_0_3():
	try:
		migrate(
			migrator.rename_column('git_setting', 'period', 'time')
		)
	except Exception as e:
		if e.args[0] == 'no such column: "period"' or str(e) == '(1060, no such column: "period")':
			print("Updating... DB has been updated to version 8.2")
		elif e.args[0] == "'bool' object has no attribute 'sql'":
			print("Updating... DB has been updated to version 8.2")
		else:
			print("An error occurred:", e)


def update_db_v_8_1_2():
	try:
		migrate(
			migrator.rename_column('settings', 'group', 'group_id'),
		)
	except Exception as e:
		if e.args[0] == 'no such column: "group"' or 'column "group" does not exist' in str(e) or str(e) == '(1060, no such column: "group")':
			print("Updating... DB has been updated to version 8.1.2")
		elif e.args[0] == "'bool' object has no attribute 'sql'":
			print("Updating... DB has been updated to version 8.1.2")
		else:
			print("An error occurred:", e)


def update_db_v_8_1_4():
	try:
		migrate(
			migrator.add_column('cred', 'private_key', TextField(null=True)),
		)
	except Exception as e:
		if (e.args[0] == 'duplicate column name: private_key' or 'column "private_key" of relation "cred" already exists'
				or str(e) == '(1060, "Duplicate column name \'private_key\'")'):
			print('Updating... DB has been updated to version 8.1.4')
		else:
			print("An error occurred:", e)


def update_db_v_8_1_6():
	try:
		if mysql_enable:
			migrate(
				migrator.add_column('udp_balancers', 'is_checker', IntegerField(default=0)),
			)
		else:
			migrate(
				migrator.add_column('udp_balancers', 'is_checker', IntegerField(constraints=[SQL('DEFAULT 0')])),
			)
	except Exception as e:
		if (e.args[0] == 'duplicate column name: is_checker' or 'column "is_checker" of relation "udp_balancers" already exists'
				or str(e) == '(1060, "Duplicate column name \'is_checker\'")'):
			print('Updating... DB has been updated to version 8.1.6')
		else:
			print("An error occurred:", e)


def update_ver():
	try:
		Version.update(version='8.1.7').execute()
	except Exception:
		print('Cannot update version')


def check_ver():
	try:
		ver = Version.get()
	except Exception as e:
		print(str(e))
	else:
		return ver.version


def update_all():
	if check_ver() is None:
		update_db_v_3_4_5_22()
	update_db_v_4_3_0()
	update_db_v_7_2_0()
	update_db_v_7_2_0_1()
	update_db_v_7_2_3()
	update_db_v_7_3_1()
	update_db_v_7_4()
	update_db_v_8()
	update_db_v_8_0_2()
	update_db_v_8_0_2_1()
	update_db_v_8_1()
	update_db_v_8_1_0_1()
	update_db_v_8_1_0_2()
	update_db_v_8_1_0_3()
	update_db_v_8_1_2()
	update_db_v_8_1_4()
	update_db_v_8_1_6()
	update_ver()
