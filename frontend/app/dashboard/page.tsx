"use client";
import { useEffect, useState } from "react";

const API_URL = "http://localhost:8000";

interface Gene {
  symbol: string;
  full_name: string;
  chromosome: string;
  role: string;
  risk_level: string;
}

interface Biomarker {
  name: string;
  type: string;
  sample_source: string;
  clinical_significance: string;
}

interface Disease {
  id: number;
  name: string;
  category: string;
  description: string;
  affected_region: string;
  prevalence: string;
  onset_age: string;
  genes: Gene[];
  biomarkers: Biomarker[];
}

interface Prediction {
  prediction: string;
  confidence_percent: number;
  all_probabilities: Record<string, number>;
  top_features: Record<string, number>;
  explanation: string;
  model_accuracy: number;
  disclaimer: string;
}

const colorMap: Record<string, string> = {
  "Alzheimer's Disease": "emerald",
  "Parkinson's Disease": "blue",
  "ALS": "purple",
  "Huntington's Disease": "orange",
};

const borderMap: Record<string, string> = {
  emerald: "border-emerald-500/40 hover:border-emerald-500",
  blue: "border-blue-500/40 hover:border-blue-500",
  purple: "border-purple-500/40 hover:border-purple-500",
  orange: "border-orange-500/40 hover:border-orange-500",
};

const textMap: Record<string, string> = {
  emerald: "text-emerald-400",
  blue: "text-blue-400",
  purple: "text-purple-400",
  orange: "text-orange-400",
};

const bgMap: Record<string, string> = {
  emerald: "bg-emerald-500/10",
  blue: "bg-blue-500/10",
  purple: "bg-purple-500/10",
  orange: "bg-orange-500/10",
};

export default function Dashboard() {
  const [diseases, setDiseases] = useState<Disease[]>([]);
  const [selected, setSelected] = useState<Disease | null>(null);
  const [loading, setLoading] = useState(true);
  const [apiStatus, setApiStatus] = useState<"checking" | "online" | "offline">("checking");
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [predicting, setPredicting] = useState(false);
  const [biomarkers, setBiomarkers] = useState({
    amyloid_beta_42: 450,
    phospho_tau_181: 420,
    neurofilament_light: 1900,
    alpha_synuclein: 1150,
    dopamine_transporter: 72,
    sod1_activity: 88,
    huntingtin_mutant: 48,
    glial_fibrillary_acidic_protein: 210,
    brain_derived_neurotrophic_factor: 13,
    inflammatory_index: 7.5,
  });

  useEffect(() => {
    checkAPI();
    fetchDiseases();
  }, []);

  async function checkAPI() {
    try {
      const res = await fetch(`${API_URL}/health`);
      if (res.ok) setApiStatus("online");
      else setApiStatus("offline");
    } catch {
      setApiStatus("offline");
    }
  }

  async function fetchDiseases() {
    try {
      const res = await fetch(`${API_URL}/diseases/`);
      const data = await res.json();
      setDiseases(data);
      if (data.length > 0) setSelected(data[0]);
    } catch {
      console.error("Failed to fetch diseases");
    } finally {
      setLoading(false);
    }
  }

  async function runPrediction() {
    setPredicting(true);
    setPrediction(null);
    try {
      const res = await fetch(`${API_URL}/ai/predict/disease`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(biomarkers),
      });
      const data = await res.json();
      setPrediction(data);
    } catch {
      console.error("Prediction failed");
    } finally {
      setPredicting(false);
    }
  }

  const color = selected ? (colorMap[selected.name] || "emerald") : "emerald";

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <div className="border-b border-gray-800 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <a href="/" className="text-gray-400 hover:text-white text-sm transition-colors">← Home</a>
          <span className="text-gray-600">/</span>
          <span className="text-white font-semibold">Research Dashboard</span>
        </div>
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${apiStatus === "online" ? "bg-emerald-400 animate-pulse" : apiStatus === "offline" ? "bg-red-400" : "bg-yellow-400"}`}></div>
          <span className="text-sm text-gray-400">API {apiStatus}</span>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Disease Knowledge Base</h1>
          <p className="text-gray-400">Live data from NeuroRegen AI API — {diseases.length} diseases loaded</p>
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-20">
            <div className="text-emerald-400 text-lg animate-pulse">Loading biological data...</div>
          </div>
        ) : (
          <div className="grid grid-cols-12 gap-6">
            <div className="col-span-3">
              <div className="space-y-3">
                {diseases.map((disease) => {
                  const c = colorMap[disease.name] || "emerald";
                  return (
                    <button key={disease.id} onClick={() => setSelected(disease)} className={`w-full text-left p-4 rounded-xl border transition-all ${selected?.id === disease.id ? `${bgMap[c]} ${borderMap[c]}` : "bg-gray-900 border-gray-800 hover:border-gray-700"}`}>
                      <div className={`text-sm font-semibold ${selected?.id === disease.id ? textMap[c] : "text-white"}`}>{disease.name}</div>
                      <div className="text-xs text-gray-500 mt-1">{disease.genes.length} genes · {disease.biomarkers.length} biomarkers</div>
                    </button>
                  );
                })}
              </div>

              <div className="mt-6 p-4 bg-gray-900 border border-gray-800 rounded-xl">
                <div className="text-xs text-gray-500 mb-2">Platform Stats</div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm"><span className="text-gray-400">Diseases</span><span className="text-emerald-400 font-mono">{diseases.length}</span></div>
                  <div className="flex justify-between text-sm"><span className="text-gray-400">Total Genes</span><span className="text-emerald-400 font-mono">{diseases.reduce((a, d) => a + d.genes.length, 0)}</span></div>
                  <div className="flex justify-between text-sm"><span className="text-gray-400">Biomarkers</span><span className="text-emerald-400 font-mono">{diseases.reduce((a, d) => a + d.biomarkers.length, 0)}</span></div>
                  <div className="flex justify-between text-sm"><span className="text-gray-400">API Status</span><span className="text-emerald-400 font-mono">{apiStatus}</span></div>
                </div>
              </div>
            </div>

            <div className="col-span-9 space-y-6">
              {selected && (
                <>
                  <div className={`p-6 rounded-xl border ${bgMap[color]} ${borderMap[color]}`}>
                    <div className="flex items-start justify-between mb-4">
                      <div>
                        <h2 className={`text-2xl font-bold ${textMap[color]}`}>{selected.name}</h2>
                        <div className="text-gray-400 text-sm mt-1">{selected.category}</div>
                      </div>
                      <div className="text-right">
                        <div className="text-xs text-gray-500">Prevalence</div>
                        <div className="text-sm text-white">{selected.prevalence}</div>
                        <div className="text-xs text-gray-500 mt-1">Onset Age</div>
                        <div className="text-sm text-white">{selected.onset_age}</div>
                      </div>
                    </div>
                    <p className="text-gray-300 text-sm leading-relaxed mb-4">{selected.description}</p>
                    <div className="flex items-center gap-2">
                      <span className="text-xs text-gray-500">Affected region:</span>
                      <span className={`text-xs px-2 py-1 rounded-full ${bgMap[color]} ${textMap[color]}`}>{selected.affected_region}</span>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-6">
                    <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
                      <h3 className="font-semibold text-white mb-4 flex items-center gap-2">
                        <span className={`w-2 h-2 rounded-full ${textMap[color].replace("text", "bg")}`}></span>
                        Associated Genes ({selected.genes.length})
                      </h3>
                      <div className="space-y-3">
                        {selected.genes.map((gene, i) => (
                          <div key={i} className="p-3 bg-gray-800 rounded-lg">
                            <div className="flex items-center justify-between mb-1">
                              <span className={`font-mono font-bold text-sm ${textMap[color]}`}>{gene.symbol}</span>
                              <span className={`text-xs px-2 py-0.5 rounded-full ${gene.risk_level === "High" ? "bg-red-500/20 text-red-400" : "bg-yellow-500/20 text-yellow-400"}`}>{gene.risk_level} risk</span>
                            </div>
                            <div className="text-xs text-gray-400 mb-1">{gene.full_name}</div>
                            <div className="text-xs text-gray-500">Chr {gene.chromosome} · {gene.role?.slice(0, 80)}...</div>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
                      <h3 className="font-semibold text-white mb-4">Biomarkers ({selected.biomarkers.length})</h3>
                      <div className="space-y-3">
                        {selected.biomarkers.map((bm, i) => (
                          <div key={i} className="p-3 bg-gray-800 rounded-lg">
                            <div className="flex items-center justify-between mb-1">
                              <span className="font-semibold text-sm text-white">{bm.name}</span>
                              <span className="text-xs bg-blue-500/20 text-blue-400 px-2 py-0.5 rounded-full">{bm.type}</span>
                            </div>
                            <div className="text-xs text-gray-400 mb-1">Source: {bm.sample_source}</div>
                            <div className="text-xs text-gray-500">{bm.clinical_significance?.slice(0, 100)}...</div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </>
              )}

              <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
                <h3 className="font-bold text-white text-lg mb-2">AI Biomarker Predictor</h3>
                <p className="text-gray-400 text-sm mb-6">Input biomarker levels to predict the most likely neurodegenerative disease using our Random Forest AI model.</p>

                <div className="grid grid-cols-2 gap-4 mb-6">
                  {Object.entries(biomarkers).map(([key, value]) => (
                    <div key={key}>
                      <label className="text-xs text-gray-400 mb-1 block">{key.replace(/_/g, " ")}</label>
                      <input type="number" value={value} onChange={(e) => setBiomarkers(prev => ({ ...prev, [key]: parseFloat(e.target.value) || 0 }))} className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-emerald-500" />
                    </div>
                  ))}
                </div>

                <button onClick={runPrediction} disabled={predicting} className="w-full bg-emerald-500 text-black font-semibold py-3 rounded-lg hover:bg-emerald-400 transition-colors disabled:opacity-50 disabled:cursor-not-allowed">
                  {predicting ? "Running AI Analysis..." : "Run Disease Prediction"}
                </button>

                {prediction && (
                  <div className="mt-6 p-5 bg-gray-800 rounded-xl border border-emerald-500/30">
                    <div className="flex items-center justify-between mb-4">
                      <div>
                        <div className="text-xs text-gray-400 mb-1">Predicted Disease</div>
                        <div className="text-xl font-bold text-emerald-400">{prediction.prediction}</div>
                      </div>
                      <div className="text-right">
                        <div className="text-xs text-gray-400 mb-1">Confidence</div>
                        <div className="text-2xl font-bold text-white">{prediction.confidence_percent}%</div>
                      </div>
                    </div>

                    <p className="text-sm text-gray-300 mb-4">{prediction.explanation}</p>

                    <div className="mb-4">
                      <div className="text-xs text-gray-400 mb-2">All Disease Probabilities</div>
                      {Object.entries(prediction.all_probabilities).map(([disease, prob]) => (
                        <div key={disease} className="flex items-center gap-3 mb-2">
                          <div className="text-xs text-gray-400 w-40 shrink-0">{disease}</div>
                          <div className="flex-1 bg-gray-700 rounded-full h-2">
                            <div className="bg-emerald-500 h-2 rounded-full transition-all" style={{ width: `${prob}%` }}></div>
                          </div>
                          <div className="text-xs text-white w-10 text-right">{prob}%</div>
                        </div>
                      ))}
                    </div>

                    <div>
                      <div className="text-xs text-gray-400 mb-2">Top Biomarker Features (Explainable AI)</div>
                      {Object.entries(prediction.top_features).map(([feature, importance]) => (
                        <div key={feature} className="flex items-center gap-3 mb-2">
                          <div className="text-xs font-mono text-emerald-400 w-48 shrink-0">{feature}</div>
                          <div className="flex-1 bg-gray-700 rounded-full h-2">
                            <div className="bg-blue-500 h-2 rounded-full" style={{ width: `${importance}%` }}></div>
                          </div>
                          <div className="text-xs text-white w-10 text-right">{importance}%</div>
                        </div>
                      ))}
                    </div>

                    <div className="mt-4 p-3 bg-yellow-500/10 border border-yellow-500/20 rounded-lg">
                      <p className="text-xs text-yellow-400">{prediction.disclaimer}</p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}