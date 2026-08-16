"use client";

import { useEffect, useState } from "react";

type Model = {
  name: string;
  artifacts_present: boolean;
  tracking_uri: string;
};

type Drift = {
  status: string;
  samples: number;
  drift_detected: boolean;
  current_phishing_rate?: number;
  z_score?: number;
};

const apiBase = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8044";

export default function MLOpsDashboard() {
  const [model, setModel] = useState<Model | null>(null);
  const [drift, setDrift] = useState<Drift | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    async function loadDashboard() {
      try {
        const [modelResponse, driftResponse] = await Promise.all([
          fetch(`${apiBase}/mlops/model`),
          fetch(`${apiBase}/mlops/drift`),
        ]);

        if (!modelResponse.ok || !driftResponse.ok) {
          throw new Error("Dashboard API unavailable");
        }

        setModel(await modelResponse.json());
        setDrift(await driftResponse.json());
        setError(false);
      } catch {
        setError(true);
      }
    }

    loadDashboard();

    const interval = setInterval(loadDashboard, 5000);
    return () => clearInterval(interval);
  }, []);

  if (error) {
    return (
      <p className="mt-12 text-center text-sm text-amber-700">
        Model monitor is unavailable. Start the FastAPI backend.
      </p>
    );
  }

  const driftLabel =
    drift?.status === "insufficient_data"
      ? "Collecting data"
      : drift?.drift_detected
        ? "Review required"
        : "Stable";

  return (
    <section className="mt-12 max-w-5xl mx-auto text-left">
      <h2 className="text-2xl font-semibold text-zinc-800">
        Security model dashboard
      </h2>

      <p className="mt-2 text-zinc-600">
        Updates automatically every 5 seconds.
      </p>

      <div className="mt-5 grid gap-4 md:grid-cols-3">
        <Card
          label="Model"
          value={model?.artifacts_present ? "Ready" : "Not trained"}
          good={Boolean(model?.artifacts_present)}
        />

        <Card
          label="Drift"
          value={driftLabel}
          good={!drift?.drift_detected}
        />

        <Card
          label="Classified emails"
          value={String(drift?.samples ?? 0)}
          good
        />
      </div>

      {drift?.current_phishing_rate !== undefined && (
        <p className="mt-4 text-sm text-zinc-600">
          Phishing rate: {Math.round(drift.current_phishing_rate * 100)}% ·
          Drift score: {drift.z_score}
        </p>
      )}
    </section>
  );
}

function Card({
  label,
  value,
  good,
}: {
  label: string;
  value: string;
  good: boolean;
}) {
  return (
    <div className="rounded-xl border border-zinc-200 bg-white p-5 shadow-sm">
      <p className="text-sm text-zinc-500">{label}</p>
      <p
        className={`mt-2 text-xl font-semibold ${
          good ? "text-emerald-700" : "text-rose-700"
        }`}
      >
        {value}
      </p>
    </div>
  );
}