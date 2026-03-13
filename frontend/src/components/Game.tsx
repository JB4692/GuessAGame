import SearchBar from "./SearchBar.tsx";
import Guess from "./Guess.tsx";
import { useEffect, useState } from "react";
import GameImage from "./GameImage.tsx";
import Lifelines from "./Lifelines.tsx";
import GameSummary from "./GameSummary.tsx";

const API_URL = import.meta.env.VITE_API_URL;
// const API_URL = "http://localhost:8000";

interface GameData {
    id: number;
    gameId: number;
    coverUrl: string;
    title: string;
    genre: string;
    platform: string;
    releaseDate: number;
    summary: string;
    rating: number;
}

const Game = () => {
    const [guesses, setGuesses] = useState<string[]>([]);
    const [titles, setTitles] = useState<string[]>([]);
    const [data, setData] = useState<GameData | null>(null);
    const [isGuessCorrect, setisGuessCorrect] = useState(false);
    const [rerollCount, setRerollCount] = useState(0);
    const [isRerolled, setRerolled] = useState(false);
    const [showSummary, setShowSummary] = useState(false);

    const reroll = () => {
        if (!isRerolled) {
            setRerollCount(rerollCount + 1);
            setRerolled(true);
            console.log("reroll called:", isRerolled, rerollCount);
        }
    };

    const addGuess = (guess: string) => {
        if (guess.toLowerCase() === answer?.toLowerCase()) {
            setisGuessCorrect(true);
        }
        setGuesses([...guesses, guess]);
    };

    useEffect(() => {
        const fetchData = async () => {
            const res = await fetch(`${API_URL}/game`);
            const json = await res.json();
            console.log(json);
            setData(json.data);
        };
        fetchData();

        const fetchTitles = async () => {
            const res = await fetch(`${API_URL}/titles`);
            const json = await res.json();
            // console.log("titles json:", json);
            setTitles(json.data.map((item: string) => item));
        };
        fetchTitles();
    }, []);

    /*
    TODO:
    Life Lines
    Image Minimap : shows where the section is on the image
    More Data : gives platforms, release date, genre
    Summary : Gives the summary of the game -> might have to scrub out the game's name though
    */

    const answer = data?.title;

    return (
        <>
            <div className="main-container">
                <div className="game-container">
                    <h1>Guess-A-Game</h1>
                    <GameImage
                        coverUrl={data?.coverUrl ?? ""}
                        guessCount={guesses.length}
                        isGuessCorrect={isGuessCorrect}
                        isRerolled={isRerolled}
                    ></GameImage>
                    <span>Guesses: {guesses.length} / 5</span>
                    <div className="search-bar-container">
                        <SearchBar
                            options={titles}
                            onGuess={addGuess}
                            guessCount={guesses.length}
                        ></SearchBar>
                        <Lifelines
                            reroll={reroll}
                            rerollCount={0}
                            isRerolled={isRerolled}
                            onShowSummary={() => {
                                setShowSummary(true);
                            }}
                            showSummary={showSummary}
                        ></Lifelines>
                    </div>

                    {guesses
                        .map((guess, index) => {
                            return <Guess key={index} title={guess} answer={answer}></Guess>;
                        })
                        .reverse()}
                </div>
                {/* <GameSummary Game={data}></GameSummary> */}
                <div className="lifelines-info-container">
                    {showSummary && data && <GameSummary Game={data}></GameSummary>}
                </div>
            </div>
        </>
    );
};

export default Game;
