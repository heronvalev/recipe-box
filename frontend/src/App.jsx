import { useEffect, useState } from 'react'
import './App.css'
import RecipeCard from './components/RecipeCard'
import RecipeForm from './components/RecipeForm'

function App() {
  const [recipes, setRecipes] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [errorMessage, setErrorMessage] = useState('')
  const [ingredientFilter, setIngredientFilter] = useState('')

  function fetchRecipes() {
    setIsLoading(true)
    setErrorMessage('')

    let url = 'http://127.0.0.1:8000/recipes'
    const cleanedIngredientFilter = ingredientFilter.trim()

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
  }

  useEffect(() => {
    fetchRecipes()
  }, [])

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
          value={ingredientFilter}
          onChange={(event) => setIngredientFilter(event.target.value)}
        />
        <button type="button" onClick={fetchRecipes}>
          Search
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