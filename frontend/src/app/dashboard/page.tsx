"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { AppHeader } from "@/components/AppHeader";
import { translations } from "@/lib/i18n";
import { useAuthStore } from "@/store/authStore";
import { useLocaleStore } from "@/store/localeStore";
import { usePlanStore } from "@/store/planStore";

const SPRITE_WIDTH = "28vmin";
const SPRITE_HEIGHT = "35vmin";

export default function DashboardPage() {
  const router = useRouter();
  const token = useAuthStore((s) => s.token);
  const locale = useLocaleStore((s) => s.locale);
  const t = translations[locale];
  const { plans, loading, fetchPlans } = usePlanStore();

  const [isSoilHovered, setIsSoilHovered] = useState(false);
  const [cursor, setCursor] = useState({ x: 0, y: 0 });

  const spiritPositions = useMemo(() => {
    const count = plans.length;
    if (count === 0) return [];

    let cols = Math.ceil(Math.sqrt(count));
    if (count <= cols) cols = count;

    const rows = Math.ceil(count / cols);
    const positions = [];
    const leftMin = 20;
    const leftMax = 80;
    const topMin = 20;
    const topMax = 80;
    const colSpacing = (leftMax - leftMin) / (cols - 1 || 1);
    const rowSpacing = (topMax - topMin) / (rows - 1 || 1);
    const staggerOffset = colSpacing * 0.3;
    const maxRandomOffsetX = colSpacing * 0.2;
    const maxRandomOffsetY = rowSpacing * 0.2;

    for (let i = 0; i < count; i++) {
      const row = Math.floor(i / cols);
      const col = i % cols;
      const baseLeftPct = leftMin + col * colSpacing + (row % 2 === 0 ? 0 : staggerOffset);
      const baseTopPct = topMin + row * rowSpacing;
      const randomOffsetX = (Math.random() * 2 - 1) * maxRandomOffsetX;
      const randomOffsetY = (Math.random() * 2 - 1) * maxRandomOffsetY;
      let leftPct = baseLeftPct + randomOffsetX;
      let topPct = baseTopPct + randomOffsetY;
      leftPct = Math.min(Math.max(leftPct, leftMin), leftMax);
      topPct = Math.min(Math.max(topPct, topMin), topMax);
      positions.push({ leftPct, topPct });
    }
    return positions;
  }, [plans]);

  const handleSoilMouseMove = (event: React.MouseEvent<HTMLDivElement>) => {
    const rect = event.currentTarget.getBoundingClientRect();
    setCursor({
      x: event.clientX - rect.left,
      y: event.clientY - rect.top,
    });
  };

  const handleSoilClick = (event: React.MouseEvent<HTMLDivElement>) => {
    const target = event.target as HTMLElement;
    const imgElement = target.closest('img[data-spirit-index]') as HTMLImageElement | null;
    if (imgElement) {
      const index = parseInt(imgElement.dataset.spiritIndex!, 10);
      router.push(`/study/${plans[index].id}`);
    } else {
      router.push("/create");
    }
  };

  const getSpiritImageSrc = (imgPrefix: string | undefined, planStatus: string) => {
    if (!imgPrefix) return '';
    if (planStatus === "CREATED") {
      return '/seed.png';
    } else if (planStatus === "STARTED") {
      return '/germinate.png';
    } else if (planStatus == "ONGOING") {
      return `/spirits/${imgPrefix}_normal.png`;
    } else if (planStatus == "STAGNANT") {
      return `/spirits/${imgPrefix}_wither.png`;
    } else {
      return `/spirits/${imgPrefix}_mature.png`;
    }
  };

  useEffect(() => {
    if (!token) {
      router.replace("/login");
      return;
    }
    fetchPlans();
  }, [token, router, fetchPlans]);

  return (
    <div
      className="relative min-h-screen overflow-hidden text-soil"
      style={{
        backgroundImage: "url('/dashboard.png')",
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
      }}
    >
      <AppHeader />
      <div
        className="absolute inset-x-0 z-0 cursor-none"
        style={{
          top: "58%",
          height: "28%",
        }}
        onMouseEnter={() => setIsSoilHovered(true)}
        onMouseMove={handleSoilMouseMove}
        onMouseLeave={() => {
          setIsSoilHovered(false);
          setCursor({ x: 0, y: 0 });
        }}
        onClick={handleSoilClick}
      >
        {isSoilHovered && (
          <div
            className="absolute pointer-events-none z-10"
            style={{
              left: `${cursor.x}px`,
              top: `${cursor.y}px`,
              transform: "translate(-52%, -72%) rotate(-25deg)",
            }}
          >
            <img
              src="/shovel.png"
              className="w-52 h-52 object-contain opacity-90 drop-shadow-lg"
            />
          </div>
        )}

        {plans.map((plan, index) => {
          const pos = spiritPositions[index];
          if (!pos) return null;

          return (
            <div
              key={plan.id}
              className="absolute"
              style={{
                left: `${pos.leftPct}%`,
                top: `${pos.topPct}%`,
                width: SPRITE_WIDTH,
                height: SPRITE_HEIGHT,
                transform: "translate(-50%, -50%)",
              }}
            >
              <img
                src={getSpiritImageSrc(plan.spirit?.img_prefix, plan.status)}
                className="w-full h-full object-contain drop-shadow-lg pointer-events-auto cursor-pointer"
                data-spirit-index={index}
                onMouseEnter={() => setIsSoilHovered(false)}
                onMouseLeave={() => setIsSoilHovered(true)}
              />
              <div
                className="absolute inset-x-0 top-1 flex justify-center pointer-events-none"
                style={{ zIndex: 5 }}
              >
                <span
                  className="text-xs md:text-sm font-medium text-white bg-black/50 px-2 py-1 rounded-full whitespace-nowrap overflow-hidden text-ellipsis max-w-full"
                  style={{ maxWidth: "90%" }}
                >
                  {locale === "en" ? plan.spirit?.name_en : plan.spirit?.name}
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {loading && (
        <p className="fixed bottom-10 left-1/2 -translate-x-1/2 text-sm text-primary/50 z-20">
          {t.dashboardLoading}
        </p>
      )}
    </div>
  );
}