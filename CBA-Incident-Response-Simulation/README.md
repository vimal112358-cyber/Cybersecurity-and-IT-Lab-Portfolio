
# 🚨 Commonwealth Bank Incident Response: Spear-Phishing & Malware Outbreak
**Virtual Internship Project | Commonwealth Bank (via Forage)**

## 📌 Incident Scenario Overview
In this simulated enterprise security incident, an attacker executed a targeted **spear-phishing campaign** against 62 employees in the Risk Department under the pretext of an urgent HR timesheet approval. The attack escalated from **credential harvesting** through a spoofed login portal to **malware deployment**, ultimately corrupting and locking corporate network file-shares.

## 🛠️ Frameworks & Technical Concepts
* **Framework:** NIST Cybersecurity Framework (NIST CSF) — Containment, Eradication, and Recovery
* **Threat Vectors:** Spear-Phishing, Social Engineering, Credential Theft, Malware / Ransomware Propagation
* **Key Artifacts:** Indicators of Compromise (IoCs), Compromised Account Credentials, Spoofed Domains

## 🔍 Incident Timeline & Triage
* **10:30 AM — Initial Alert:** An employee reported a suspicious HR timesheet link that threw a server error after credential entry.
* **2:00 PM — Scope Expansion:** Investigation confirmed 62 Risk Department colleagues received the email, directing them to a fake site that harvested credentials and downloaded a harmful program.
* **3:50 PM — Critical Impact:** Network file-shares became inaccessible and Word documents threw opening errors, signaling active malware propagation and file encryption.

## 🛡️ Strategic Containment & Recovery Plan

### 1. Containment Actions
* **Endpoint Isolation:** Disconnected infected workstations from the internal network to prevent lateral movement.
* **File-Share Severing:** Temporarily took affected network file-shares offline to arrest further malware file encryption.
* **Credential Revocation:** Immediately disabled user accounts, revoked active session tokens, and forced password resets for all 62 targeted employees.
* **Gateway Filtering:** Blacklisted malicious domains, IP addresses, and file hashes across firewalls and email security gateways.

### 2. Eradication & Recovery
* **Endpoint Remediation:** Scanned and purged malware using Endpoint Detection & Response (EDR) tools, reimaging severely compromised systems.
* **Clean Data Restoration:** Restored corrupted files on network shares from clean, verified offline backups.
* **Access Restoration:** Enforced Multi-Factor Authentication (MFA) prior to restoring user network permissions.

### 3. Post-Incident & Lessons Learned
* **Root Cause Analysis (RCA):** Conducted a deep dive into email gateway policies to patch filtering gaps.
* **Security Awareness:** Scheduled targeted phishing simulations and anti-phishing awareness sessions for high-risk corporate departments.

---

### 📬 Contact
* **LinkedIn:** [vimal-k-0765783a4](https://linkedin.com/in/vimal-k-0765783a4)[cite: 1]
* **Email:** vimal.112358@gmail.com[cite: 1]
