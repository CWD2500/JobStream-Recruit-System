# 💼 JobStream: Enterprise Recruitment Management System

> **A robust, full-stack recruitment solution bridging the gap between professional talent and industry leaders through advanced RDBMS architecture and seamless UX.**

---

## 📖 Executive Summary
**JobStream** is an integrated strategic tool designed to streamline the hiring lifecycle. It serves as a high-efficiency link between job seekers and employers, replacing traditional, fragmented processes with a modern, automated ecosystem that prioritizes data integrity and user interaction[cite: 1].

---

## 🏛️ System Architecture & Database Design
The project’s backbone is a sophisticated **Relational Database Management System (RDBMS)** consisting of **12 normalized tables**[cite: 1]. 

### 🖼️ Conceptual Diagram
The following diagram illustrates the complex relationships between users, job entities, and the notification engine:

![Conceptual Diagram](./docs/conceptual-diagram.png)

*Key Engineering Highlights:*
* **Multi-Entity Seeker Profiles**: Normalized tables for Education, Experience, Skills, and Certificates[cite: 1].
* **Application Bridge**: A Many-to-Many logic implementation connecting seekers to job postings[cite: 1].
* **Bidirectional Notification Logic**: An automated system tracking `sender_id` and `receiver_id` to facilitate real-time feedback[cite: 1].

---

## 🚀 Key Features

### 👤 For Job Seekers
* **Dynamic CV Builder**: Interactive profile creation incorporating qualifications and professional milestones[cite: 1].
* **Advanced Discovery**: Multi-criteria search filters (Location, Specialty, Job Type, Experience Level)[cite: 1].
* **One-Click Application**: Direct document upload and submission tracking[cite: 1].

### 🏢 For Employers
* **Listing Management**: Complete CRUD operations for job advertisements with dynamic status updates[cite: 1].
* **Applicant Tracking System (ATS)**: Centralized dashboard for reviewing resumes and managing candidate pipelines[cite: 1].
* **Direct Feedback Loop**: Immediate communication of acceptance or rejection with custom instructions[cite: 1].

### 🛠️ For Administrators
* **Market Adaptation**: Tools to modify job sectors and system settings according to market changes[cite: 1].
* **Security & Governance**: Comprehensive user oversight and data protection protocols[cite: 1].

---

## 📊 Operational Workflow (The SDLC Approach)
The system operates through a strictly defined hierarchy of roles to ensure security and efficiency[cite: 1]:

1. **Authentication**: Role-based login (Seeker, Employer, Admin) unlocks specific system permissions[cite: 1].
2. **The Engagement Cycle**: 
   * Employers post requirements → Seekers filter and apply → System triggers instant notifications[cite: 1].
3. **Decision Phase**: Employers review detailed digital profiles → Status updates (Accept/Reject) are reflected in the Seeker's "My Applications" portal[cite: 1].

---

## 🛡️ System Constraints & Business Rules
To maintain professional standards, the system enforces the following:
* **Role Integrity**: Seekers cannot post jobs; Employers cannot apply for jobs[cite: 1].
* **Data Privacy**: Restricted access to user data based on pre-defined permissions[cite: 1].
* **Transactional Reliability**: Notifications are strictly tied to database status changes for 100% accuracy[cite: 1].
* **File Validation**: Strict controls on file types and sizes for CV uploads[cite: 1].

---

## 🛠️ Technical Stack
* **Language/Framework**: Python / Django (Backend Logic)
* **Database**: MySQL (12 Interconnected Tables)[cite: 1]
* **Analysis Tools**: Use Case, Activity, Class, and Conceptual Diagrams[cite: 1]
* **Communication**: Integrated Email & In-app Notification Engine[cite: 1]
