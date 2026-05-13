import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [recipes, setRecipes] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [errorMessage, setErrorMessage] = useState('')

  useEffect(() => {
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
  }, [])

  return (
    <main className="app">
      <h1>Recipe Box</h1>
      <p>A simple frontend for managing recipes.</p>

      {isLoading && <p>Loading recipes...</p>}

      {errorMessage && <p>{errorMessage}</p>}

      {!isLoading && !errorMessage && (
        <ul>
          {recipes.map((recipe) => (
            <li key={recipe.id}>{recipe.title}</li>
          ))}
        </ul>
      )}
    </main>
  )
}

export default App