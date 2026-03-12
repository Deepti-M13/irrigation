import { Cpu, Satellite, BrainCircuit, BellRing } from "lucide-react";
import { ScrollReveal, StaggerContainer, StaggerItem } from "./ScrollReveal";

const SolutionsSection = ({ id, t }) => {
  const solutions = [
    {
      icon: Cpu,
      title: t('s1_t'),
      desc: t('s1_d'),
    },
    {
      icon: Satellite,
      title: t('s2_t'),
      desc: t('s2_d'),
    },
    {
      icon: BrainCircuit,
      title: t('s3_t'),
      desc: t('s3_d'),
    },
    {
      icon: BellRing,
      title: t('s4_t'),
      desc: t('s4_d'),
    },
  ];

  return (
    <section id={id} className="py-24 bg-background">
      <div className="container">
        <ScrollReveal>
          <p className="text-xs font-semibold uppercase tracking-[0.25em] text-primary mb-3">
            {t('sol_tag')}
          </p>
        </ScrollReveal>
        <ScrollReveal delay={0.1}>
          <h2 className="font-display text-3xl md:text-4xl font-extrabold mb-4 max-w-lg">
            {t('sol_title')}
          </h2>
        </ScrollReveal>
        <ScrollReveal delay={0.2}>
          <p className="text-muted-foreground text-base mb-14 max-w-xl">
            {t('sol_desc')}
          </p>
        </ScrollReveal>
        <StaggerContainer className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {solutions.map((s, i) => (
            <StaggerItem key={i}>
              <div className="group rounded-xl border border-border bg-card p-6 hover:border-primary/30 hover:shadow-lg hover:shadow-primary/5 transition-all duration-300 h-full">
                <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mb-5 group-hover:bg-primary/20 transition-colors">
                  <s.icon className="w-6 h-6 text-primary" />
                </div>
                <h3 className="font-display font-bold text-base mb-2">{s.title}</h3>
                <p className="text-muted-foreground text-sm leading-relaxed">{s.desc}</p>
              </div>
            </StaggerItem>
          ))}
        </StaggerContainer>
      </div>
    </section>
  );
};

export default SolutionsSection;
