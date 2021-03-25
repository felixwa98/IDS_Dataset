# IDS_Dataset
The intrusion detection dataset contains 10 days of networkflows, which are mostly generated with the attached Python Script. The user activities include surfing the Internet, VoIP phone calls, SSH, FTP and writing e-mails. The configuration of every activity can be adjusted within the config folder. 
 

The different labels indicate the following classifcation of the networkflow:

| Classification | Label |
| --- | --- | 
| Benign | 0 |
| Reverse Shell | 1 |
| Malware | 2 |
| C2 | 3 |
| Botnet DDOS | 4 |
| Botnet Spam | 5 |
| Crypto Miner | 6 |
| Huge Data Transfer | 7 |



The data set contains the following attributes:

| Attribute |
| --- |
| Source IP |
| Source Port |
| Destination IP |
| Destination Port |
| Starttime |
| TCP Flags |
| Size |
| Packets |
| Protocol |
| Type |
| Version |
| Label |
