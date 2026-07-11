import Navbar from "@/components/Navbar";
import Hero from "@/components/Hero";
import Diseases from "@/components/Diseases";
import Tools from "@/components/Tools";
import Roadmap from "@/components/Roadmap";
import Footer from "@/components/Footer";

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-950 text-white">
      <Navbar />
      <Hero />
      <Diseases />
      <Tools />
      <Roadmap />
      <Footer />
    </main>
  );
}
