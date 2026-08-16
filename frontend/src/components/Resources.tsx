"use client";

export default function Resources() {
  const youtubeUrl = process.env.NEXT_PUBLIC_YOUTUBE_URL;

  return (
    <section className="bg-white py-20">
      <div className="max-w-5xl mx-auto px-6 text-center space-y-14">
        {/* Main heading */}
        <div className="space-y-4">
          <h2 className="text-4xl md:text-5xl font-light tracking-wide bg-gradient-to-r from-purple-600 to-pink-500 bg-clip-text text-transparent">
            Project Resources
          </h2>
          <p className="text-gray-600 text-lg max-w-2xl mx-auto">
            Watch the{" "}
            <span className="font-medium text-purple-600">video demo</span>,
            explore the repositories and the
            <span className="font-medium text-pink-500">
              {" "}
              API documentation
            </span>
            .
          </p>
        </div>

        {/* YouTube player */}
        {youtubeUrl ? (
          <div className="aspect-video w-full rounded-2xl overflow-hidden shadow-xl ring-1 ring-gray-200 hover:ring-purple-300 transition">
            <iframe
              src={youtubeUrl}
              title="Email Classifier Demo"
              className="w-full h-full"
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
          </div>
        ) : (
          <div className="text-sm text-gray-500 italic">
            🔒 Video URL not configured (add in{" "}
            <code>.env.local → NEXT_PUBLIC_YOUTUBE_URL</code>)
          </div>
        )}

        {/* Main links */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-8 mt-12">
          <a
            href="https://apiemailclassifier.flipafile.com/docs#"
            target="_blank"
            rel="noopener noreferrer"
            className="p-8 border rounded-2xl shadow-sm bg-gray-50 hover:shadow-lg hover:-translate-y-1 hover:border-purple-300 transition transform duration-300"
          >
            <h3 className="font-light text-xl text-purple-600 tracking-wide">
              Swagger API
            </h3>
            <p className="text-base text-gray-600 mt-3">
              Interactive FastAPI documentation.
            </p>
          </a>

          <a
            href="https://github.com/4snt/email-classifier-frontend"
            target="_blank"
            rel="noopener noreferrer"
            className="p-8 border rounded-2xl shadow-sm bg-gray-50 hover:shadow-lg hover:-translate-y-1 hover:border-purple-300 transition transform duration-300"
          >
            <h3 className="font-light text-xl text-purple-600 tracking-wide">
              Frontend Repo
            </h3>
            <p className="text-base text-gray-600 mt-3">
              Frontend code in Next.js + Tailwind.
            </p>
          </a>

          <a
            href="https://github.com/4snt/email-classifier"
            target="_blank"
            rel="noopener noreferrer"
            className="p-8 border rounded-2xl shadow-sm bg-gray-50 hover:shadow-lg hover:-translate-y-1 hover:border-purple-300 transition transform duration-300"
          >
            <h3 className="font-light text-xl text-purple-600 tracking-wide">
              Backend Repo
            </h3>
            <p className="text-base text-gray-600 mt-3">
              FastAPI with hexagonal architecture.
            </p>
          </a>
        </div>
      </div>
    </section>
  );
}
