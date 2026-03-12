import { Droplets, Sprout, BarChart3 } from "lucide-react";
import { ScrollReveal, StaggerContainer, StaggerItem } from "./ScrollReveal";

const ImpactSection = ({ t }) => {
  const stats = [
    {
      icon: Droplets,
      value: t('i1_v'),
      label: t('i1_l'),
      desc: t('i1_d'),
    },
    {
      icon: Sprout,
      value: t('i2_v'),
      label: t('i2_l'),
      desc: t('i2_d'),
    },
    {
      icon: BarChart3,
      value: t('i3_v'),
      label: t('i3_l'),
      desc: t('i3_d'),
    },
  ];

  return (
    <section className="py-24 bg-background">
      <div className="container">
        <ScrollReveal className="text-center mb-14">
          <p className="text-xs font-semibold uppercase tracking-[0.25em] text-primary mb-3">
            {t('imp_tag')}
          </p>
          <h2 className="font-display text-3xl md:text-4xl font-extrabold mb-4">
            {t('imp_title')}
          </h2>
          <p className="text-muted-foreground text-sm max-w-lg mx-auto">
            {t('imp_desc')}
          </p>
        </ScrollReveal>
        <StaggerContainer className="grid md:grid-cols-3 gap-8">
          {stats.map((s, i) => (
            <StaggerItem key={i}>
              <div className="text-center rounded-xl border border-border bg-card p-8 hover:border-primary/20 transition-colors h-full">
                <div className="w-14 h-14 rounded-2xl bg-primary/10 flex items-center justify-center mx-auto mb-5">
                  <s.icon className="w-7 h-7 text-primary" />
                </div>
                <p className="font-display text-3xl font-extrabold text-primary mb-1">{s.value}</p>
                <p className="font-display font-bold text-base mb-2">{s.label}</p>
                <p className="text-muted-foreground text-sm">{s.desc}</p>
              </div>
            </StaggerItem>
          ))}
        </StaggerContainer>
      </div>
    </section>
  );
};

export default ImpactSection;
