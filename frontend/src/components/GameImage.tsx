import { useState, useEffect } from "react";

interface GameImageProps {
    coverUrl: string;
    guessCount: number;
    isGuessCorrect: boolean;
    isRerolled: boolean;
}

const GameImage = ({ coverUrl, guessCount, isGuessCorrect, isRerolled }: GameImageProps) => {
    const [position, setPosition] = useState<{ x: number; y: number } | null>(null);
    const [imageSize, setImageSize] = useState<{ w: number; h: number } | null>(null);

    const currSize = 200 + guessCount * 100;

    useEffect(() => {
        if (isRerolled || !position) {
            setPosition({ x: Math.random(), y: Math.random() });
        }
    }, [isRerolled]);

    useEffect(() => {
        const img = new Image();
        img.src = coverUrl;
        img.onload = () => {
            setImageSize({ w: img.naturalWidth, h: img.naturalHeight });
        };
    }, [coverUrl]);

    if (!position || !imageSize) return null;

    const posX = position.x * (imageSize.w - currSize);
    const posY = position.y * (imageSize.h - currSize);

    if (isGuessCorrect || guessCount >= 5) {
        return <img src={coverUrl} style={{ width: imageSize.w / 2, height: imageSize.h / 2 }} />;
    }

    return (
        <div
            style={{
                width: currSize,
                height: currSize,
                backgroundImage: `url(${coverUrl})`,
                backgroundPosition: `-${posX}px -${posY}px`,
                backgroundRepeat: "no-repeat",
                backgroundSize: `${imageSize.w}px ${imageSize.h}px`,
            }}
        />
    );
};

export default GameImage;
