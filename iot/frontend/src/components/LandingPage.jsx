import Navbar from "./Navbar";
import HeroSection from "./HeroSection";
import ImpactSection from "./ImpactSection";
import ProblemSection from "./ProblemSection";
import SolutionsSection from "./SolutionsSection";
import FeaturesSection from "./FeaturesSection";
import DashboardPreview from "./DashboardPreview";
import HowItWorks from "./HowItWorks";
import AudienceSection from "./AudienceSection";
import CTASection from "./CTASection";
import Footer from "./Footer";

const LandingPage = ({ currentLang, changeLanguage, t, onLogin }) => {
  return (
    <div className="min-h-screen bg-background text-foreground font-sans selection:bg-primary/20">
      <Navbar 
        currentLang={currentLang} 
        changeLanguage={changeLanguage} 
        t={t} 
        onLogin={onLogin}
      />
      <main>
        <HeroSection t={t} onGetStarted={onLogin} />
        <ImpactSection t={t} />
        <ProblemSection t={t} />
        <SolutionsSection id="solutions" t={t} />
        <FeaturesSection id="features" t={t} />
        <DashboardPreview id="dashboard-preview" t={t} />
        <HowItWorks id="how-it-works" t={t} />
        <AudienceSection t={t} />
        <CTASection onGetStarted={onLogin} t={t} />
      </main>
      <Footer t={t} />
    </div>
  );
};

export default LandingPage;
