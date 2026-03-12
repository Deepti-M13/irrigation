import { useState } from "react";
import { Menu, X } from "lucide-react";
import { Button } from "@/components/ui/button";

const Navbar = ({ onLogin, onGetStarted, currentLang, changeLanguage, t }) => {
  const navItems = [
    { label: t('solutions'), id: 'solutions' },
    { label: t('features'), id: 'features' },
    { label: t('howItWorks'), id: 'how-it-works' },
    { label: t('dashboard'), id: 'dashboard' }
  ];
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-md border-b border-border">
      <div className="container flex items-center justify-between h-16">
        <span className="font-display text-xl font-extrabold tracking-tight text-primary">
          GraminLink
        </span>

        {/* Desktop */}
        <div className="hidden md:flex items-center gap-8">
          {navItems.map((item) => (
            <a
              key={item.id}
              href={`#${item.id}`}
              className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
            >
              {item.label}
            </a>
          ))}
        </div>

        <div className="hidden md:flex items-center gap-3">
          <div className="hidden lg:flex bg-secondary/50 p-1 rounded-xl border border-border mr-2 overflow-x-auto max-width-[400px]">
            {['English', 'Hindi', 'Telugu', 'Tamil', 'Malayalam', 'Kannada', 'Marathi', 'Bengali', 'Gujarati'].map((lang) => (
              <button
                key={lang}
                onClick={() => changeLanguage(lang)}
                className={`px-2 py-1 rounded-lg text-[9px] font-bold uppercase tracking-wider transition-all whitespace-nowrap ${currentLang === lang ? 'bg-primary text-primary-foreground shadow-sm' : 'text-muted-foreground hover:text-foreground'}`}
              >
                {lang.substring(0, 3)}
              </button>
            ))}
          </div>
          <Button variant="ghost" size="sm" className="text-muted-foreground hover:text-foreground" onClick={onLogin}>
            {t('login')}
          </Button>
          <Button size="sm" onClick={onGetStarted}>{t('getStarted')}</Button>
        </div>

        {/* Mobile toggle */}
        <button
          className="md:hidden text-foreground"
          onClick={() => setMobileOpen(!mobileOpen)}
        >
          {mobileOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {/* Mobile menu */}
      {mobileOpen && (
        <div className="md:hidden bg-background border-b border-border px-6 pb-6 animate-fade-in">
          {navItems.map((item) => (
            <a
              key={item.id}
              href={`#${item.id}`}
              onClick={() => setMobileOpen(false)}
              className="block py-3 text-sm font-medium text-muted-foreground hover:text-foreground"
            >
              {item.label}
            </a>
          ))}
          <div className="flex flex-wrap gap-2 my-4 p-2 bg-secondary/30 rounded-xl">
            {['English', 'Hindi', 'Telugu', 'Tamil', 'Malayalam', 'Kannada', 'Marathi', 'Bengali', 'Gujarati'].map((lang) => (
              <button
                key={lang}
                onClick={() => changeLanguage(lang)}
                className={`flex-1 min-w-[70px] px-2 py-2 rounded-lg text-[10px] font-bold uppercase tracking-wider transition-all ${currentLang === lang ? 'bg-primary text-primary-foreground' : 'text-muted-foreground bg-background/50'}`}
              >
                {lang}
              </button>
            ))}
          </div>
          <div className="flex gap-3 mt-4">
            <Button variant="ghost" size="sm" className="w-full text-muted-foreground" onClick={onLogin}>{t('login')}</Button>
            <Button size="sm" className="w-full" onClick={onGetStarted}>{t('getStarted')}</Button>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
