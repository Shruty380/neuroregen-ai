export default function Hero() {
  return (
    <section className="min-h-screen flex items-center justify-center px-6 pt-20">
      <div className="max-w-4xl mx-auto text-center">
        <div className="inline-flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/20 rounded-full px-4 py-2 text-emerald-400 text-sm mb-8">
          <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></div>
          AI-Powered Bioinformatics Research Platform
        </div>
        <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
          Decoding
          <span className="text-emerald-400"> Neurodegeneration</span>
          <br />with AI
        </h1>
        <p className="text-xl text-gray-400 mb-10 max-w-2xl mx-auto leading-relaxed">
          An open research platform combining bioinformatics, machine learning,
          and regenerative biology to study Alzheimer's, Parkinson's, ALS,
          and Huntington's disease.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <a href="#diseases" className="bg-emerald-500 text-black px-8 py-4 rounded-lg font-semibold text-lg hover:bg-emerald-400 transition-colors">Explore Research</a>
          <a href="https://github.com/Shruty380/neuroregen-ai" target="_blank" rel="noreferrer" className="border border-gray-700 text-white px-8 py-4 rounded-lg font-semibold text-lg hover:border-emerald-500 transition-colors">View on GitHub</a>
        </div>
        <div className="mt-16 grid grid-cols-3 gap-8 max-w-lg mx-auto">
          <div className="text-center">
            <div className="text-3xl font-bold text-emerald-400">4</div>
            <div className="text-gray-500 text-sm mt-1">Diseases Studied</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-emerald-400">8</div>
            <div className="text-gray-500 text-sm mt-1">Research Phases</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-emerald-400">AI</div>
            <div className="text-gray-500 text-sm mt-1">Powered Analysis</div>
          </div>
        </div>
      </div>
    </section>
  );
}