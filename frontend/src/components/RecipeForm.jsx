import { useState } from 'react'

// Display a form for creating a new recipe.
function RecipeForm() {
  const [title, setTitle] = useState('')
  const [instructions, setInstructions] = useState('')
  const [ingredientName, setIngredientName] = useState('')
  const [ingredientQuantity, setIngredientQuantity] = useState('')
  const [ingredientUnit, setIngredientUnit] = useState('')

  function handleSubmit(event) {
    event.preventDefault()

    console.log({
      title: title,
      instructions: instructions,
      ingredients: [
        {
          name: ingredientName,
          quantity: ingredientQuantity,
          unit: ingredientUnit,
        },
      ],
    })
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>Add a recipe</h2>

      <div>
        <label htmlFor="title">Title</label>
        <input
          id="title"
          type="text"
          value={title}
          onChange={(event) => setTitle(event.target.value)}
        />
      </div>

      <div>
        <label htmlFor="instructions">Instructions</label>
        <textarea
          id="instructions"
          value={instructions}
          onChange={(event) => setInstructions(event.target.value)}
        />
      </div>

      <fieldset>
        <legend>Ingredient</legend>

        <div>
          <label htmlFor="ingredient-name">Name</label>
          <input
            id="ingredient-name"
            type="text"
            value={ingredientName}
            onChange={(event) => setIngredientName(event.target.value)}
          />
        </div>

        <div>
          <label htmlFor="ingredient-quantity">Quantity</label>
          <input
            id="ingredient-quantity"
            type="text"
            value={ingredientQuantity}
            onChange={(event) => setIngredientQuantity(event.target.value)}
          />
        </div>

        <div>
          <label htmlFor="ingredient-unit">Unit</label>
          <input
            id="ingredient-unit"
            type="text"
            value={ingredientUnit}
            onChange={(event) => setIngredientUnit(event.target.value)}
          />
        </div>
      </fieldset>

      <button type="submit">Add recipe</button>
    </form>
  )
}

export default RecipeForm