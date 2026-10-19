# 🚨 Commonwealth Bank Security Simulation: Incident Response & Awareness
**Virtual Internship Project | Commonwealth Bank (via Forage)**

## 📌 Incident Scenario Overview
In this simulated enterprise security incident, an attacker executed a targeted **spear-phishing campaign** against 62 employees in the Risk Department under the pretext of an urgent HR timesheet approval. The attack escalated from **credential harvesting** through a spoofed login portal to **malware deployment**, ultimately corrupting and locking corporate network file-shares.

## 🛠️ Frameworks & Technical Concepts
* **Framework:** NIST Cybersecurity Framework (NIST CSF) — Containment, Eradication, and Recovery
* **Threat Vectors:** Spear-Phishing, Social Engineering, Credential Theft, Malware / Ransomware Propagation
* **Key Artifacts:** Indicators of Compromise (IoCs), Compromised Account Credentials, Spoofed Domains

---

## 🔍 Tasks 1 & 2: Incident Timeline, Triage & Containment

### Incident Timeline
* **10:30 AM — Initial Alert:** An employee reported a suspicious HR timesheet link that threw a server error after credential entry.
* **2:00 PM — Scope Expansion:** Investigation confirmed 62 Risk Department colleagues received the email, directing them to a fake site that harvested credentials and downloaded a harmful program.
* **3:50 PM — Critical Impact:** Network file-shares became inaccessible and Word documents threw opening errors, signaling active malware propagation and file encryption.

### Strategic Containment & Recovery Plan
1. **Endpoint & Network Isolation:** Disconnected infected workstations and temporarily severed network file-shares to halt lateral malware movement.
2. **Credential Revocation:** Disabled accounts, revoked active tokens, and forced password resets for all 62 targeted employees.
3. **Gateway Filtering:** Blacklisted malicious domains, IP addresses, and file hashes across firewalls and email gateways.
4. **Data Restoration:** Scanned endpoints with EDR tools and restored corrupted files from clean, offline backups.

---

## 🎨 Task 3: Security Awareness & Password Policy Infographic

### 📌 Overview
To mitigate future credential harvesting and social engineering risks identified during the incident, I designed an enterprise security awareness infographic based on **Australian Cyber Security Centre (ACSC)** guidelines for bank employees.

### 🔑 Key Concepts Covered
- **Passphrase Strategy:** Transitioning from complex short passwords to 4+ random word passphrases (e.g., `purple-koala-laptop-sunset!`).
- **Multi-Factor Authentication (MFA):** Highlighting MFA as a critical secondary defense against stolen credentials.
- **Enterprise Password Management:** Promoting approved password managers over reused or written-down passwords.

### 📄 Deliverable View
- **[View Password Security Infographic PDF](./Password Security Infographic.pdf)**

---

### 📬 Contact
* **LinkedIn:** [vimal-k-0765783a4](https://linkedin.com/in/vimal-k-0765783a4)
* **Email:** vimal.112358@gmail.com
