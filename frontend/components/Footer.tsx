export default function Footer() {
  return (
    <footer className="border-t border-gray-800 py-12 px-6">
      <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 bg-emerald-500 rounded flex items-center justify-center text-black font-bold text-xs">NR</div>
          <span className="text-white font-semibold">NeuroRegen AI</span>
        </div>
        <p className="text-gray-500 text-sm text-center">
          Built by Shruty · Biotechnology graduate exploring AI and Computational Biology
        </p>
        <a href="https://github.com/Shruty380/neuroregen-ai" target="_blank" rel="noreferrer" className="text-emerald-400 text-sm hover:text-emerald-300 transition-colors">github.com/Shruty380</a>
      </div>
    </footer>
  );
}