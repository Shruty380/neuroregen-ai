const diseases = [
  { name: "Alzheimer's Disease", description: "Progressive memory loss caused by amyloid plaques and tau tangles destroying neurons in the hippocampus and cortex.", gene: "APOE4, APP, PSEN1", color: "emerald" },
  { name: "Parkinson's Disease", description: "Loss of dopaminergic neurons in the substantia nigra, causing motor dysfunction through alpha-synuclein aggregation.", gene: "SNCA, LRRK2, PINK1", color: "blue" },
  { name: "ALS", description: "Motor neuron degeneration affecting both upper and lower motor neurons, leading to progressive muscle paralysis.", gene: "SOD1, C9orf72, FUS", color: "purple" },
  { name: "Huntington's Disease", description: "CAG repeat expansion in the HTT gene produces toxic huntingtin protein that destroys striatal neurons.", gene: "HTT (CAG repeats)", color: "orange" },
];

const colorMap: Record<string, string> = {
  emerald: "border-emerald-500/30 hover:border-emerald-500",
  blue: "border-blue-500/30 hover:border-blue-500",
  purple: "border-purple-500/30 hover:border-purple-500",
  orange: "border-orange-500/30 hover:border-orange-500",
};

const badgeMap: Record<string, string> = {
  emerald: "bg-emerald-500/10 text-emerald-400",
  blue: "bg-blue-500/10 text-blue-400",
  purple: "bg-purple-500/10 text-purple-400",
  orange: "bg-orange-500/10 text-orange-400",
};

export default function Diseases() {
  return (
    <section id="diseases" className="py-24 px-6">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">Disease Research Focus</h2>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">Studying the molecular mechanisms of four major neurodegenerative diseases using genomic and proteomic data analysis.</p>
        </div>
        <div className="grid md:grid-cols-2 gap-6">
          {diseases.map((disease) => (
            <div key={disease.name} className={`bg-gray-900 border ${colorMap[disease.color]} rounded-xl p-6 transition-colors duration-300`}>
              <h3 className="text-xl font-bold text-white mb-3">{disease.name}</h3>
              <p className="text-gray-400 text-sm leading-relaxed mb-4">{disease.description}</p>
              <div className={`inline-flex items-center gap-2 ${badgeMap[disease.color]} rounded-full px-3 py-1 text-xs font-mono`}>Key genes: {disease.gene}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}