import Link from "next/link"
import Image from "next/image"
import { Button } from "@/components/ui/button"
import { Clock, DollarSign, Fuel, MapPin, BarChart3, Users, Route, TrendingDown } from "lucide-react"

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-600 via-purple-600 to-indigo-800">
      {/* Header */}
      <header className="container mx-auto py-6 px-4 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <Route className="h-8 w-8 text-white" />
          <span className="text-xl font-bold text-white">BusOptimize</span>
        </div>
        <nav className="hidden md:flex gap-6">
          <Link href="/" className="text-white hover:text-indigo-200 transition">
            Home
          </Link>
          <Link href="/optimizer" className="text-white hover:text-indigo-200 transition">
            Optimizer
          </Link>
          <Link href="#services" className="text-white hover:text-indigo-200 transition">
            Services
          </Link>
          <Link href="#contact" className="text-white hover:text-indigo-200 transition">
            Contact
          </Link>
        </nav>
        <Button variant="outline" className="bg-white/10 text-white border-white/20 hover:bg-white/20">
          Login
        </Button>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-16 md:py-24 flex flex-col md:flex-row items-center">
        <div className="md:w-1/2 text-center md:text-left mb-10 md:mb-0">
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-white leading-tight mb-6">
            Smart Bus Route <span className="text-indigo-200">Optimizer</span>
          </h1>
          <p className="text-xl text-white/80 mb-8 max-w-lg">
            Save time, fuel, and money with our intelligent bus route optimization system. Perfect for schools and
            transportation companies.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center md:justify-start">
            <Button asChild size="lg" className="bg-white text-indigo-700 hover:bg-indigo-100">
              <Link href="/optimizer">Start Optimizing</Link>
            </Button>
            <Button
              asChild
              variant="outline"
              size="lg"
              className="bg-transparent border-white text-white hover:bg-white/20"
            >
              <Link href="#services">Learn More</Link>
            </Button>
          </div>
        </div>
        <div className="md:w-1/2 flex justify-center">
          <div className="relative w-full max-w-md h-80">
            <Image
              src="/main-bg.png?height=400&width=500"
              alt="Bus Route Optimization"
              fill
              className="object-contain"
              priority
            />
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="bg-white/10 backdrop-blur-sm py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center text-white mb-12">Why Choose Our Solution?</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {/* Benefit 1 */}
            <div className="bg-white/10 rounded-xl p-6 backdrop-blur-sm border border-white/20 hover:bg-white/20 transition">
              <div className="bg-indigo-600 w-12 h-12 rounded-full flex items-center justify-center mb-4">
                <Fuel className="h-6 w-6 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Save Fuel</h3>
              <p className="text-white/80">
                Optimize routes to minimize distance traveled, reducing fuel consumption by up to 30%.
              </p>
            </div>

            {/* Benefit 2 */}
            <div className="bg-white/10 rounded-xl p-6 backdrop-blur-sm border border-white/20 hover:bg-white/20 transition">
              <div className="bg-indigo-600 w-12 h-12 rounded-full flex items-center justify-center mb-4">
                <Clock className="h-6 w-6 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Save Time</h3>
              <p className="text-white/80">
                Reduce travel time with efficient routing algorithms that find the shortest paths possible.
              </p>
            </div>

            {/* Benefit 3 */}
            <div className="bg-white/10 rounded-xl p-6 backdrop-blur-sm border border-white/20 hover:bg-white/20 transition">
              <div className="bg-indigo-600 w-12 h-12 rounded-full flex items-center justify-center mb-4">
                <DollarSign className="h-6 w-6 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Save Money</h3>
              <p className="text-white/80">
                Cut operational costs through reduced fuel usage, vehicle maintenance, and driver hours.
              </p>
            </div>

            {/* Benefit 4 */}
            <div className="bg-white/10 rounded-xl p-6 backdrop-blur-sm border border-white/20 hover:bg-white/20 transition">
              <div className="bg-indigo-600 w-12 h-12 rounded-full flex items-center justify-center mb-4">
                <TrendingDown className="h-6 w-6 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Reduce Costs</h3>
              <p className="text-white/80">
                Lower your overall transportation budget with smarter resource allocation and planning.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section id="services" className="container mx-auto px-4 py-16 md:py-24">
        <h2 className="text-3xl font-bold text-center text-white mb-4">Our Services</h2>
        <p className="text-center text-white/80 mb-12 max-w-2xl mx-auto">
          Comprehensive solutions to make your transportation system more efficient and cost-effective
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Service 1 */}
          <div className="bg-white/10 rounded-xl p-8 backdrop-blur-sm border border-white/20 flex gap-6">
            <div className="bg-indigo-600 w-16 h-16 rounded-full flex-shrink-0 flex items-center justify-center">
              <Route className="h-8 w-8 text-white" />
            </div>
            <div>
              <h3 className="text-xl font-semibold text-white mb-2">Optimize Routes</h3>
              <p className="text-white/80">
                Our advanced algorithms analyze multiple factors including traffic patterns, road conditions, and
                student locations to create the most efficient routes possible, saving time and resources.
              </p>
            </div>
          </div>

          {/* Service 2 */}
          <div className="bg-white/10 rounded-xl p-8 backdrop-blur-sm border border-white/20 flex gap-6">
            <div className="bg-indigo-600 w-16 h-16 rounded-full flex-shrink-0 flex items-center justify-center">
              <Users className="h-8 w-8 text-white" />
            </div>
            <div>
              <h3 className="text-xl font-semibold text-white mb-2">Allocate Students</h3>
              <p className="text-white/80">
                Intelligently assign students to buses based on location, capacity, and special requirements, ensuring
                balanced loads and minimizing travel time for each student.
              </p>
            </div>
          </div>

          {/* Service 3 */}
          <div className="bg-white/10 rounded-xl p-8 backdrop-blur-sm border border-white/20 flex gap-6">
            <div className="bg-indigo-600 w-16 h-16 rounded-full flex-shrink-0 flex items-center justify-center">
              <MapPin className="h-8 w-8 text-white" />
            </div>
            <div>
              <h3 className="text-xl font-semibold text-white mb-2">Monitor Routes</h3>
              <p className="text-white/80">
                Track and analyze route performance in real-time, allowing for quick adjustments when needed and
                providing insights for continuous improvement of your transportation system.
              </p>
            </div>
          </div>

          {/* Service 4 */}
          <div className="bg-white/10 rounded-xl p-8 backdrop-blur-sm border border-white/20 flex gap-6">
            <div className="bg-indigo-600 w-16 h-16 rounded-full flex-shrink-0 flex items-center justify-center">
              <BarChart3 className="h-8 w-8 text-white" />
            </div>
            <div>
              <h3 className="text-xl font-semibold text-white mb-2">Cost Analysis</h3>
              <p className="text-white/80">
                Comprehensive reporting tools that break down transportation costs, identify savings opportunities, and
                help you make data-driven decisions to optimize your budget.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-indigo-900 py-16">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">Ready to Optimize Your Bus Routes?</h2>
          <p className="text-white/80 mb-8 max-w-2xl mx-auto">
            Join hundreds of schools and transportation companies that have reduced costs and improved efficiency with
            our solution.
          </p>
          <Button asChild size="lg" className="bg-white text-indigo-700 hover:bg-indigo-100">
            <Link href="/optimizer">Get Started Now</Link>
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-indigo-950 py-12">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center gap-2 mb-6 md:mb-0">
              <Route className="h-8 w-8 text-white" />
              <span className="text-xl font-bold text-white">BusOptimize</span>
            </div>
            <div className="flex flex-col md:flex-row gap-8">
              <div>
                <h3 className="text-white font-semibold mb-3">Quick Links</h3>
                <ul className="space-y-2">
                  <li>
                    <Link href="/" className="text-white/70 hover:text-white transition">
                      Home
                    </Link>
                  </li>
                  <li>
                    <Link href="/optimizer" className="text-white/70 hover:text-white transition">
                      Optimizer
                    </Link>
                  </li>
                  <li>
                    <Link href="#services" className="text-white/70 hover:text-white transition">
                      Services
                    </Link>
                  </li>
                </ul>
              </div>
              <div>
                <h3 className="text-white font-semibold mb-3">Contact</h3>
                <ul className="space-y-2">
                  <li className="text-white/70">info@busoptimize.com</li>
                  <li className="text-white/70">+1 (555) 123-4567</li>
                </ul>
              </div>
            </div>
          </div>
          <div className="border-t border-white/20 mt-8 pt-8 text-center text-white/60">
            <p>© {new Date().getFullYear()} BusOptimize. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

