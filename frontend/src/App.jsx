import { useEffect, useState } from 'react'
import './App.css'
import RecipeCard from './components/RecipeCard'
import RecipeForm from './components/RecipeForm'

function App() {
  const [recipes, setRecipes] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [errorMessage, setErrorMessage] = useState('')

  function fetchRecipes() {
    setIsLoading(true)
    setErrorMessage('')

    fetch('http://127.0.0.1:8000/recipes')
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

      {isLoading && <p>Loading recipes...</p>}

      {errorMessage && <p>{errorMessage}</p>}

      {!isLoading && !errorMessage && (
        <ul className="recipe-list">
          {recipes.map((recipe) => (
            <RecipeCard key={recipe.id} recipe={recipe} />
          ))}
        </ul>
      )}
    </main>
  )
}

export default App