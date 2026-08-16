"use client";

import { useEffect, useState } from "react";
import { fetchLogs, type LogItem } from "@/lib/api";

export default function ClassificationHistory() {
  const [logs, setLogs] = useState<LogItem[]>([]);
  const [loading, setLoading] = useState(true);

  async function loadLogs() {
    const result = await fetchLogs({ limit: 20 });
    if (result) setLogs(result);
    setLoading(false);
  }

  useEffect(() => {
    loadLogs();

  }, []);

  return (
    <section className="mt-12 max-w-5xl mx-auto text-left">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-semibold text-zinc-800">
            Classification History
          </h2>
          <p className="mt-1 text-sm text-zinc-600">
            Results refresh automatically every 5 seconds.
          </p>
        </div>

        <button
          onClick={loadLogs}
          className="rounded-lg bg-zinc-900 px-4 py-2 text-sm font-medium text-white"
        >
          Refresh
        </button>
      </div>

      <div className="mt-5 overflow-x-auto rounded-xl border border-zinc-200 bg-white">
        <table className="w-full text-sm">
          <thead className="bg-zinc-100 text-left text-zinc-700">
            <tr>
              <th className="p-3">Processed</th>
              <th className="p-3">Email</th>
              <th className="p-3">Result</th>
              <th className="p-3">Reason</th>
            </tr>
          </thead>

          <tbody>
            {loading && (
              <tr>
                <td colSpan={4} className="p-5 text-center text-zinc-500">
                  Loading classifications…
                </td>
              </tr>
            )}

            {!loading && logs.length === 0 && (
              <tr>
                <td colSpan={4} className="p-5 text-center text-zinc-500">
                  No classified emails yet.
                </td>
              </tr>
            )}

            {logs.map((log) => (
              <tr key={log.id} className="border-t border-zinc-100">
                <td className="p-3 text-zinc-600">
                  {new Date(log.created_at).toLocaleString()}
                </td>

                <td className="p-3">
                  <p className="font-medium text-zinc-900">
                    {log.subject || "(No subject)"}
                  </p>
                  <p className="text-xs text-zinc-500">
                    {log.sender || "Unknown sender"}
                  </p>
                </td>

                <td className="p-3">
                  <span
                    className={`rounded-full px-3 py-1 text-xs font-semibold ${
                      log.category === "unproductive"
                        ? "bg-red-100 text-red-700"
                        : "bg-emerald-100 text-emerald-700"
                    }`}
                  >
                    {log.category === "unproductive"
                      ? "Unproductive"
                      : "Productive"}
                  </span>
                </td>

                <td className="max-w-sm p-3 text-zinc-600">
                  {log.reason || "No explanation available"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}