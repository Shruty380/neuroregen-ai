const tools = [
  { name: "BLAST Alignment", desc: "Compare DNA/protein sequences against biological databases", tag: "Bioinformatics" },
  { name: "Gene Expression AI", desc: "ML models trained on RNA-seq data to detect disease signatures", tag: "AI/ML" },
  { name: "Biomarker Prediction", desc: "Predict early-stage disease biomarkers from genomic profiles", tag: "AI/ML" },
  { name: "Pathway Analysis", desc: "Map genes to biological pathways and identify disrupted networks", tag: "Bioinformatics" },
  { name: "Literature Mining", desc: "NLP-powered extraction of insights from PubMed research papers", tag: "AI/ML" },
  { name: "Drug Target Ranking", desc: "Score and rank potential therapeutic targets using graph analysis", tag: "Research" },
];

export default function Tools() {
  return (
    <section id="tools" className="py-24 px-6 bg-gray-900/50">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">Platform Tools</h2>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">A suite of bioinformatics and AI tools built specifically for neurodegenerative disease research.</p>
        </div>
        <div className="grid md:grid-cols-3 gap-6">
          {tools.map((tool) => (
            <div key={tool.name} className="bg-gray-900 border border-gray-800 rounded-xl p-6 hover:border-emerald-500/50 transition-colors">
              <div className="text-xs font-medium text-emerald-400 bg-emerald-500/10 rounded-full px-3 py-1 inline-block mb-4">{tool.tag}</div>
              <h3 className="font-bold text-white mb-2">{tool.name}</h3>
              <p className="text-gray-400 text-sm leading-relaxed">{tool.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}