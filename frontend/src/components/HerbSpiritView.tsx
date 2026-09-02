"use client";

import { motion } from "framer-motion";
import type { HerbSpirit } from "@/lib/types";

interface Props {
  spirit: HerbSpirit;
  planStatus: string | undefined;
  size?: "sm" | "md" | "lg";
  className?: string;
}

export function HerbSpiritView({
  spirit,
  planStatus,
  size = "md",
  className = "",
}: Props) {
  const dim = size === "sm" ? 56 : size === "lg" ? 140 : 88;
  const sleeping = planStatus === "STAGNANT";

  const getSpiritImageSrc = (imgPrefix: string | undefined, planStatus: string | undefined) => {
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

  return (
    <div
      className={`relative flex flex-col justify-end items-center ${className}`}
      style={{
        width: dim,
        height: dim,
        overflow: "hidden",
      }}
    >
      <motion.div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          alignItems: "flex-end",
          justifyContent: "center",
        }}
        animate={
          sleeping
            ? { rotate: [0, -3, 0, 3, 0], y: [0, 2, 0] }
            : { y: [0, -3, 0] }
        }
        transition={{
          duration: sleeping ? 3.6 : 2.8,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      >
        <img
          src={getSpiritImageSrc(spirit.img_prefix, planStatus)}
          className="object-contain drop-shadow-lg"
          style={{
            width: "100%",
            height: "100%",
          }}
        />
      </motion.div>

      {sleeping && (
        <motion.span
          className="absolute -right-1 top-2 font-display text-xs text-wither"
          animate={{ opacity: [0.2, 1, 0.2], y: [0, -6, 0] }}
          transition={{ duration: 2.4, repeat: Infinity }}
        >
          z
        </motion.span>
      )}
    </div>
  );
}