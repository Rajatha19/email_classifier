"use client";

import profiles from "@/data/profiles.json";
import { configureImapService, stopImapService } from "@/lib/api";
import { useState } from "react";
import { toast } from "sonner";
import { Button } from "./ui/Button";

type ImapResponse = {
  status: string;
  profile_id?: string;
  interval?: number;
  mailbox?: string;
  host?: string;
};

export default function ImapForm() {
  const [form, setForm] = useState({
    host: "imap.gmail.com",
    user: "",
    password: "",
    mailbox: "INBOX",
    profile_id: "",
    interval: 10,
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ImapResponse | null>(null);
  const [file, setFile] = useState<File | null>(null); // 👈 optional file

  function handleChange(
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    try {
      const res = await configureImapService(form);
      if (!res) {
        toast.error("Error configuring IMAP");
        setLoading(false);
        return;
      }

      setResult(res);
      toast.success("IMAP service started");
    } catch (err) {
      console.error(err);
      toast.error("Unexpected error while configuring");
    } finally {
      setLoading(false);
    }
  }

  async function handleStop() {
    const res = await stopImapService();
    if (res) {
      setResult(null);
    }
  }

  return (
    <div className="mt-12 max-w-3xl mx-auto px-6">
      <h2 className="text-3xl md:text-4xl font-light tracking-wide mb-8 bg-gradient-to-r from-purple-600 to-pink-500 bg-clip-text text-transparent text-center">
        Connect via Gmail IMAP
      </h2>

      {/* Warning */}
      <div className="mb-8 p-5 bg-yellow-50 border border-yellow-200 rounded-xl text-base text-gray-700 space-y-3 shadow-sm">
        <p>
          <strong>⚠️ This prototype only works with Gmail accounts.</strong>
        </p>
        <p>
          You need to enable <strong>2FA</strong> and use an{" "}
          <strong>App Password</strong>.
        </p>
        <p>
          <a
            href="https://myaccount.google.com/apppasswords"
            target="_blank"
            rel="noopener noreferrer"
            className="text-purple-600 underline hover:text-purple-800"
          >
            👉 Click here to generate your app password
          </a>
        </p>
        <p className="text-sm text-gray-500">
          Logs are not permanent — prototype only.
        </p>
      </div>

      {/* Form */}
      <form
        onSubmit={handleSubmit}
        className="flex flex-col gap-5 bg-white p-8 rounded-2xl shadow-xl border border-gray-200 transition-all duration-300 hover:shadow-2xl"
      >
        <input
          type="text"
          name="user"
          value={form.user}
          onChange={handleChange}
          placeholder="User (e.g.: youremail@gmail.com)"
          className="border rounded-lg p-4 text-base bg-gray-50 focus:ring-2 focus:ring-purple-300 outline-none transition"
          required
        />

        <input
          type="password"
          name="password"
          value={form.password}
          onChange={handleChange}
          placeholder="App Password (16 characters)"
          className="border rounded-lg p-4 text-base bg-gray-50 focus:ring-2 focus:ring-purple-300 outline-none transition"
          required
        />

        {/* Profile selection */}
        <div className="flex flex-col text-left">
          <label
            htmlFor="profile"
            className="text-sm font-medium text-gray-700 mb-2"
          >
            Choose classification profile
          </label>
          <select
            id="profile"
            name="profile_id"
            value={form.profile_id}
            onChange={handleChange}
            className="border rounded-lg p-4 text-base bg-gray-50 focus:ring-2 focus:ring-purple-300 outline-none transition"
          >
            <option value="">Select a profile</option>
            {Object.values(profiles).slice(0, 5).map((p: any) => (
              <option key={p.id} value={p.id}>
                {p.name}
              </option>
            ))}
          </select>
        </div>

        {/* Buttons */}
        <Button
          type="submit"
          isLoading={loading}
          variant="primary"
          size="lg"
          className="w-full"
        >
          {loading ? "Connecting..." : "Start IMAP Service"}
        </Button>

        <Button
          type="button"
          onClick={handleStop}
          variant="secondary"
          size="lg"
          className="w-full"
        >
          Stop IMAP Service
        </Button>
      </form>

      {/* Result */}
      {result && (
        <div className="mt-8 p-5 rounded-xl border bg-gray-50 shadow text-left space-y-2">
          <div>
            <strong>Status:</strong> {result.status}
          </div>
          {result.profile_id && (
            <div>
              <strong>Profile:</strong> {result.profile_id}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
