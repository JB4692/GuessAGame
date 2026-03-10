import { useState, useRef, useEffect } from "react";

interface GameImageProps {
    coverUrl: string;
    guessCount: number;
    isGuessCorrect: boolean;
    rerollCount: number;
}

const GameImage = ({
    coverUrl,
    guessCount,
    isGuessCorrect,
    rerollCount,
}: GameImageProps) => {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const cropPositionRef = useRef<{ x: number; y: number } | null>(null);

    useEffect(() => {
        if (rerollCount <= 4 && !isGuessCorrect) {
            cropPositionRef.current = null;
        }
    }, [rerollCount]);

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext("2d");
        if (!ctx) return;

        const img = new Image();
        img.src = coverUrl;
        img.onload = () => {
            if (isGuessCorrect) {
                // reveal the whole image
                canvas.width = img.naturalWidth / 2;
                canvas.height = img.naturalHeight / 2;
                ctx.drawImage(
                    img,
                    0,
                    0,
                    img.naturalWidth / 2,
                    img.naturalHeight / 2,
                );
                return;
            }
            const revealSize = 50 + guessCount * 50;

            // only set random position once
            if (!cropPositionRef.current) {
                cropPositionRef.current = {
                    x: Math.floor(Math.random() * (img.width - 200)),
                    y: Math.floor(Math.random() * (img.height - 200)),
                };
            }

            const pos = cropPositionRef.current;
            ctx.drawImage(
                img,
                pos.x,
                pos.y,
                revealSize,
                revealSize,
                0,
                0,
                200,
                200,
            );
        };
    }, [guessCount, coverUrl, isGuessCorrect, rerollCount]);

    return <canvas ref={canvasRef} width={200} height={200} />;
};

export default GameImage;
