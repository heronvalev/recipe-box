// Display the details for a single recipe.
function RecipeCard({ recipe, onRecipeDeleted }) {
  async function handleDelete() {
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/recipes/${recipe.id}`,
        {
          method: 'DELETE',
        }
      )

      if (!response.ok) {
        throw new Error('Could not delete recipe.')
      }

      onRecipeDeleted()
    } catch (error) {
      console.error(error)
    }
  }

  return (
    <li className="recipe-card">
      <h2>{recipe.title}</h2>

      <p>{recipe.instructions}</p>

      <h3>Ingredients</h3>

      <ul>
        {recipe.ingredients.map((ingredient, index) => {
          const quantity = ingredient.quantity ? `${ingredient.quantity} ` : ''
          const unit = ingredient.unit ? `${ingredient.unit} ` : ''

          return (
            <li key={index}>
              {quantity}
              {unit}
              {ingredient.name}
            </li>
          )
        })}
      </ul>

      <button type="button" onClick={handleDelete}>
        Delete recipe
      </button>
      
    </li>
  )
}

export default RecipeCard