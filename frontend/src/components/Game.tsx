import SearchBar from "./SearchBar.tsx";
import Guess from "./Guess.tsx";
import { useEffect, useState } from "react";
import GameImage from "./GameImage.tsx";

interface GameData {
    game_id: number;
    cover_id: string;
    name: string;
    genres: string[];
    platforms: string[];
    release_dates: number[];
    summary: string;
    rating: number[];
    base_img: string;
    crop_img: string[];
}
const Game = () => {
    const [guesses, setGuesses] = useState<string[]>([]);
    const [titles, setTitles] = useState<string[]>([]);
    const [data, setData] = useState<GameData | null>(null);
    const [isGuessCorrect, setisGuessCorrect] = useState(false);
    const [rerollCount, setRerollCount] = useState(0);

    const reroll = () => {
        if (rerollCount < 3) {
            setRerollCount(rerollCount + 1);
        }
    };

    useEffect(() => {
        const fetchData = async () => {
            const res = await fetch("http://127.0.0.1:8000/game");
            const json = await res.json();
            console.log(json);
            setData(json.data);
        };
        fetchData();
    }, []);

    useEffect(() => {
        const fetchTitles = async () => {
            const res = await fetch("http://127.0.0.1:8000/titles");
            const json = await res.json();
            // console.log("titles json:", json);
            setTitles(json.data.map((item: string) => item));
        };
        fetchTitles();
    }, []);

    const addGuess = (guess: string) => {
        if (guess.toLowerCase() === answer?.toLowerCase()) {
            setisGuessCorrect(true);
        }
        setGuesses([...guesses, guess]);
    };

    // add a function which will loop over the images in base_img and crop_img
    // to load all the images so that they don't need to be fetched each time. :)

    const answer = data?.name;
    // console.log(answer);
    // console.log("titles ", titles);

    return (
        <div>
            <h1>Guess-A-Game</h1>
            <GameImage
                coverUrl={`https://images.igdb.com/igdb/image/upload/t_1080p/${data?.cover_id}.jpg`}
                guessCount={guesses.length}
                isGuessCorrect={isGuessCorrect}
                rerollCount={rerollCount + 1}
            ></GameImage>
            <div className="search-bar-container">
                <SearchBar options={titles} onGuess={addGuess}></SearchBar>
                <button
                    onClick={() => {
                        reroll();
                    }}
                >
                    Re-roll Image
                </button>
                <span>{rerollCount} / 3</span>
            </div>
            {guesses
                .map((guess, index) => {
                    return (
                        <Guess
                            key={index}
                            title={guess}
                            answer={answer}
                        ></Guess>
                    );
                })
                .reverse()}
        </div>
    );
};

export default Game;
