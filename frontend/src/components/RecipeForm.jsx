import { useState } from 'react'

// Display a form for creating a new recipe.
function RecipeForm() {
  const [title, setTitle] = useState('')
  const [instructions, setInstructions] = useState('')
  const [ingredients, setIngredients] = useState([
    {
      name: '',
      quantity: '',
      unit: '',
    },
  ])

  function handleIngredientChange(index, field, value) {
    const updatedIngredients = ingredients.map((ingredient, ingredientIndex) => {
      if (ingredientIndex === index) {
        return {
          ...ingredient,
          [field]: value,
        }
      }

      return ingredient
    })

    setIngredients(updatedIngredients)
  }

  function handleAddIngredient() {
    setIngredients([
      ...ingredients,
      {
        name: '',
        quantity: '',
        unit: '',
      },
    ])
  }

  async function handleSubmit(event) {
    event.preventDefault()

    const newRecipe = {
      title: title,
      instructions: instructions,
      ingredients: ingredients,
    }

    try {
      const response = await fetch('http://127.0.0.1:8000/recipes', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newRecipe),
      })

      if (!response.ok) {
        throw new Error('Could not create recipe.')
      }

      const createdRecipe = await response.json()

      console.log(createdRecipe)
    } catch (error) {
      console.error(error)
    }
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
        <legend>Ingredients</legend>

        {ingredients.map((ingredient, index) => (
          <div key={index}>
            <div>
              <label htmlFor={`ingredient-name-${index}`}>Name</label>
              <input
                id={`ingredient-name-${index}`}
                type="text"
                value={ingredient.name}
                onChange={(event) =>
                  handleIngredientChange(index, 'name', event.target.value)
                }
              />
            </div>

            <div>
              <label htmlFor={`ingredient-quantity-${index}`}>
                Quantity
              </label>
              <input
                id={`ingredient-quantity-${index}`}
                type="text"
                value={ingredient.quantity}
                onChange={(event) =>
                  handleIngredientChange(index, 'quantity', event.target.value)
                }
              />
            </div>

            <div>
              <label htmlFor={`ingredient-unit-${index}`}>Unit</label>
              <input
                id={`ingredient-unit-${index}`}
                type="text"
                value={ingredient.unit}
                onChange={(event) =>
                  handleIngredientChange(index, 'unit', event.target.value)
                }
              />
            </div>
          </div>
        ))}
      </fieldset>

      <button type="button" onClick={handleAddIngredient}>
        Add another ingredient
      </button>

      <button type="submit">Add recipe</button>
    </form>
  )
}

export default RecipeForm