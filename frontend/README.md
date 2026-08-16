# 📧 Email Classifier — Frontend (Next.js + Tailwind)

Frontend for the **AutoU Technical Challenge MVP** — web interface for the automatic email classification system.  
Allows configuring IMAP access (via Gmail), classifying received messages as **Productive** or **Unproductive**, and viewing classification logs.

🔗 **Published site:** [autou.flipafile.com](https://autou.flipafile.com/)  
👤 **Author:** [@4snt](https://github.com/4snt)

---

## ✨ Features

- Form to connect via **IMAP (Gmail + app password)**
- **Classification profile** selection
- Start and stop IMAP service directly from the interface
- File upload (`.pdf`, `.txt`) for manual classification
- Direct classification via pasted text
- Results and logs visualization
- Status feedback via notifications (Sonner)

---

## 🏗️ Stack

- **Next.js 15** + App Router
- **React 18**
- **TailwindCSS**
- **Sonner** (notifications)
- **TypeScript**
- **API Backend**: FastAPI (hexagonal + DDD-lite)

---

## 📂 Simplified Structure

```
email-classifier-frontend/
├─ src/
│  ├─ components/
│  │   ├─ ImapForm.tsx        # IMAP form (start/stop service)
│  │   ├─ ClassifierForm.tsx  # File or text upload for classification
│  │   └─ ui/                 # Buttons, inputs and UI elements
│  ├─ lib/
│  │   └─ api.ts              # FastAPI backend integration
│  ├─ data/
│  │   └─ profiles.json       # Classification profiles
│  └─ app/
│      └─ page.tsx            # Home with tabs: Gmail / Upload / Demo
├─ public/
│  └─ images/logo-autou.webp
├─ package.json
├─ tailwind.config.ts
├─ README.md
└─ .env.example
```

---

## ▶️ How to run locally

```bash
# Install dependencies
pnpm install   # or npm install

# Configure variables
cp .env.example .env

# Run in dev mode
pnpm dev       # or npm run dev
```

Access: `http://localhost:3000`

---

## 🌐 Backend Integration

- `NEXT_PUBLIC_API_URL` should point to the running FastAPI backend (e.g., `http://localhost:8000` or URL on Coolify).
- Frontend consumes routes:
  - `POST /imap/config` → starts IMAP service
  - `POST /imap/stop` → stops IMAP service
  - `GET /imap/status` → current status
  - `POST /classify` → text/file classification
  - `GET /logs` → latest logs

---

## 📍 Next Steps

- Dashboard with classification statistics
- Improve mobile responsiveness
- Multi-user authentication

---

## 📜 License

Free use for this **AutoU** technical challenge.

---

### ⚡ Repository & Deploy

- Repository: [github.com/basantiroomie/emailclassifier](https://github.com/basantiroomie/emailclassifier)
- Deploy: [autou.flipafile.com](https://autou.flipafile.com/)
