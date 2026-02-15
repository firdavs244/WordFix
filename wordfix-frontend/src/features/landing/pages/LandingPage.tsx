import { LandingNav } from '../components/LandingNav';
import { HeroSection } from '../components/HeroSection';
import { FeaturesSection } from '../components/FeaturesSection';
import { StatsBar } from '../components/StatsBar';
import { HowItWorksSection } from '../components/HowItWorksSection';
import { TestimonialsSection } from '../components/TestimonialsSection';
import { CTASection } from '../components/CTASection';
import { LandingFooter } from '../components/LandingFooter';

export function LandingPage() {
  return (
    <div className="min-h-screen overflow-hidden bg-background">
      <LandingNav />
      <HeroSection />
      <FeaturesSection />
      <StatsBar />
      <HowItWorksSection />
      <TestimonialsSection />
      <CTASection />
      <LandingFooter />
    </div>
  );
}
