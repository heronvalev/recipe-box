import { useCallback, useEffect, useState } from 'react'
import './App.css'
import RecipeCard from './components/RecipeCard'
import RecipeForm from './components/RecipeForm'

function App() {
  const [recipes, setRecipes] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [errorMessage, setErrorMessage] = useState('')
  const [ingredientFilterInput, setIngredientFilterInput] = useState('')
  const [activeIngredientFilter, setActiveIngredientFilter] = useState('')

  const fetchRecipes = useCallback(() => {
    setIsLoading(true)
    setErrorMessage('')

    let url = 'http://127.0.0.1:8000/recipes'
    const cleanedIngredientFilter = activeIngredientFilter.trim()

    if (cleanedIngredientFilter) {
      url = `http://127.0.0.1:8000/recipes?ingredient=${encodeURIComponent(cleanedIngredientFilter)}`
    }

    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        setRecipes(data)
        setIsLoading(false)
      })
      .catch(() => {
        setErrorMessage('Could not load recipes.')
        setIsLoading(false)
      })
  }, [activeIngredientFilter])

  function handleSearch() {
    setActiveIngredientFilter(ingredientFilterInput)
  }

  function handleClearFilter() {
    setIngredientFilterInput('')
    setActiveIngredientFilter('')
  }

  useEffect(() => {
    fetchRecipes()
  }, [fetchRecipes])

  return (
    <main className="app">
      <h1>Recipe Box</h1>
      <p>A simple frontend for managing recipes.</p>

      <RecipeForm onRecipeCreated={fetchRecipes} />

      <div>
        <label htmlFor="ingredient-filter">Filter by ingredient</label>

        <input
          id="ingredient-filter"
          type="text"
          value={ingredientFilterInput}
          onChange={(event) => setIngredientFilterInput(event.target.value)}
        />

        <button type="button" onClick={handleSearch}>
          Search
        </button>

        <button type="button" onClick={handleClearFilter}>
          Clear
        </button>
      </div>

      {isLoading && <p>Loading recipes...</p>}

      {errorMessage && <p>{errorMessage}</p>}

      {!isLoading && !errorMessage && (
        <ul className="recipe-list">
          {recipes.map((recipe) => (
            <RecipeCard
              key={recipe.id}
              recipe={recipe}
              onRecipeDeleted={fetchRecipes}
            />
          ))}
        </ul>
      )}
    </main>
  )
}

export default App