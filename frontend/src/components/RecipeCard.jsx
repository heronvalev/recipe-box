// Display the details for a single recipe.
function RecipeCard({ recipe }) {
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
    </li>
  )
}

export default RecipeCard