interface Config {
    flow_rate: number;
    pumps: PumpConfig;
}
interface PumpConfig {
    [k: string]: number;
}

interface Drink {
    name: string;
    recipe: Recipe;
}

type Recipe = RecipeStep[];

type RecipeStep = RecipeIngredientInstruction[];

interface RecipeIngredientInstruction {
    ingredient: string;
    volume: number;
    delay?: number;
}
