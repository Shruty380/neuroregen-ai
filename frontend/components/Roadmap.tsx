const phases = [
  { phase: "01", title: "GitHub Setup", status: "complete", desc: "Repository structure, CI/CD pipeline" },
  { phase: "02", title: "Portfolio Website", status: "active", desc: "Next.js frontend, TailwindCSS design" },
  { phase: "03", title: "Disease Knowledge Base", status: "upcoming", desc: "PostgreSQL database, FastAPI backend" },
  { phase: "04", title: "Bioinformatics Tools", status: "upcoming", desc: "BLAST, Clustal Omega, NCBI API" },
  { phase: "05", title: "AI Models", status: "upcoming", desc: "Biomarker prediction, disease classification" },
  { phase: "06", title: "Research Dashboard", status: "upcoming", desc: "Data visualization, real-time analysis" },
  { phase: "07", title: "Publication Ready", status: "upcoming", desc: "Research reports, citations, exports" },
  { phase: "08", title: "Startup Architecture", status: "upcoming", desc: "Scalable infrastructure, Docker, cloud" },
];

export default function Roadmap() {
  return (
    <section id="roadmap" className="py-24 px-6">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">Development Roadmap</h2>
          <p className="text-gray-400 text-lg">Eight phases from research platform to startup foundation.</p>
        </div>
        <div className="space-y-4">
          {phases.map((item) => (
            <div key={item.phase} className={`flex items-start gap-6 p-5 rounded-xl border transition-colors ${item.status === "complete" ? "bg-emerald-500/5 border-emerald-500/30" : item.status === "active" ? "bg-blue-500/5 border-blue-500/30" : "bg-gray-900 border-gray-800"}`}>
              <div className={`text-2xl font-bold font-mono min-w-[3rem] ${item.status === "complete" ? "text-emerald-400" : item.status === "active" ? "text-blue-400" : "text-gray-600"}`}>{item.phase}</div>
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-1">
                  <h3 className="font-bold text-white">{item.title}</h3>
                  {item.status === "complete" && <span className="text-xs bg-emerald-500/20 text-emerald-400 px-2 py-0.5 rounded-full">Complete</span>}
                  {item.status === "active" && <span className="text-xs bg-blue-500/20 text-blue-400 px-2 py-0.5 rounded-full animate-pulse">In Progress</span>}
                </div>
                <p className="text-gray-400 text-sm">{item.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}