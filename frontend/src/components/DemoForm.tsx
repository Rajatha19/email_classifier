"use client";

import profiles from "@/data/profiles.json";
import type { ClassifyResponse } from "@/lib/api";
import { classifyEmail, classifyFile } from "@/lib/api";
import { X } from "lucide-react"; // 👈 X icon
import { useRef, useState } from "react";
import { toast } from "sonner";
import { Button } from "./ui/Button";

export default function ClassifierForm() {
  const [text, setText] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<ClassifyResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [profileId, setProfileId] = useState<string>("");
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    try {
      let res: ClassifyResponse | null = null;

      if (file) {
        res = await classifyFile(file, { profileId: profileId || null });
      } else if (text.trim().length > 0) {
        res = await classifyEmail(text, { profileId: profileId || null });
      } else {
        toast.warning("No text or file provided");
        setLoading(false);
        return;
      }

      if (!res) {
        toast.error("Error classifying");
        setLoading(false);
        return;
      }

      setResult(res);

      // reset text, but keep file until user removes it
      setText("");
      if (fileInputRef.current) fileInputRef.current.value = "";

      toast.success("Classification completed!");
    } catch (err) {
      console.error(err);
      toast.error("Unexpected error while classifying");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mt-12 max-w-3xl mx-auto px-6">
      <h2 className="text-3xl md:text-4xl font-light tracking-wide mb-8 bg-gradient-to-r from-purple-600 to-pink-500 bg-clip-text text-transparent text-center">
        Test Now
      </h2>

      <form
        onSubmit={handleSubmit}
        className="flex flex-col gap-6 bg-white p-8 rounded-2xl shadow-xl border border-gray-200 transition-all duration-300 hover:shadow-2xl"
      >
        {/* Profile selector */}
        <div className="flex flex-col text-left">
          <label
            htmlFor="profile"
            className="text-sm font-medium text-gray-700 mb-2"
          >
            Choose classification profile
          </label>
          <select
            id="profile"
            value={profileId}
            onChange={(e) => setProfileId(e.target.value || "")}
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

        {/* Text field */}
        <div className="flex flex-col text-left">
          <label
            htmlFor="email-text"
            className="text-sm font-medium text-gray-700 mb-2"
          >
            Email text
          </label>
          <textarea
            id="email-text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste email content here..."
            className="border rounded-lg p-4 text-base bg-gray-50 focus:ring-2 focus:ring-purple-300 outline-none transition"
            rows={6}
          />
        </div>

        {/* File upload */}
        <div className="flex flex-col text-left">
          <label
            htmlFor="file-upload"
            className="text-sm font-medium text-gray-700 mb-2"
          >
            Or upload a file
          </label>
          <input
            id="file-upload"
            ref={fileInputRef}
            type="file"
            accept=".txt,.pdf,.eml"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="block w-full text-sm text-gray-600
                       file:mr-4 file:py-2 file:px-4
                       file:rounded-md file:border-0
                       file:text-sm file:font-medium
                       file:bg-purple-50 file:text-purple-700
                       hover:file:bg-purple-100"
          />

          {file && (
            <div className="mt-3 flex items-center justify-between bg-gray-100 px-3 py-2 rounded-lg text-sm text-gray-700">
              <span> {file.name}</span>
              <button
                type="button"
                onClick={() => {
                  setFile(null);
                  if (fileInputRef.current) fileInputRef.current.value = "";
                }}
                className="text-gray-500 hover:text-red-600 transition"
              >
                <X size={18} />
              </button>
            </div>
          )}
        </div>

        {/* Button */}
        <Button
          type="submit"
          isLoading={loading}
          variant="primary"
          size="lg"
          className="w-full"
        >
          {loading ? "Classifying..." : "Classify"}
        </Button>
      </form>

      {/* Result */}
      {result && (
        <div className="mt-8 p-5 rounded-xl border bg-gray-50 shadow text-left space-y-2">
          <div>
            <strong>Category:</strong> {result.category}
          </div>
          <div>
            <strong>Reason:</strong> {result.reason}
          </div>
          <div>
            <strong>Suggested reply:</strong> {result.suggested_reply}
          </div>
          <div className="mt-4 pt-4 border-t text-sm text-gray-600">
            <strong>Model:</strong> {result.used_model || 'ml_classifier'}
          </div>
        </div>
      )}
    </div>
  );
}
