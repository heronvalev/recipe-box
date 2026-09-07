import { useState } from 'react'

function RecipeEditForm({ recipe, onRecipeUpdated, onCancel }) {
  const [title, setTitle] = useState(recipe.title)
  const [instructions, setInstructions] = useState(recipe.instructions)
  const [ingredients, setIngredients] = useState(recipe.ingredients)

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

  return (
    <form>
      <h3>Edit recipe</h3>

      <div>
        <label htmlFor={`edit-title-${recipe.id}`}>Title</label>
        <input
          id={`edit-title-${recipe.id}`}
          type="text"
          value={title}
          onChange={(event) => setTitle(event.target.value)}
        />
      </div>

      <div>
        <label htmlFor={`edit-instructions-${recipe.id}`}>Instructions</label>
        <textarea
          id={`edit-instructions-${recipe.id}`}
          value={instructions}
          onChange={(event) => setInstructions(event.target.value)}
        />
      </div>

			<fieldset>
				<legend>Ingredients</legend>

				{ingredients.map((ingredient, index) => (
					<div key={index}>
						<div>
							<label htmlFor={`edit-ingredient-name-${recipe.id}-${index}`}>
								Name
							</label>
							<input
								id={`edit-ingredient-name-${recipe.id}-${index}`}
								type="text"
								value={ingredient.name}
								onChange={(event) =>
									handleIngredientChange(index, 'name', event.target.value)
								}
							/>
						</div>

						<div>
							<label htmlFor={`edit-ingredient-quantity-${recipe.id}-${index}`}>
								Quantity
							</label>
							<input
								id={`edit-ingredient-quantity-${recipe.id}-${index}`}
								type="text"
								value={ingredient.quantity || ''}
								onChange={(event) =>
									handleIngredientChange(index, 'quantity', event.target.value)
								}
							/>
						</div>

						<div>
							<label htmlFor={`edit-ingredient-unit-${recipe.id}-${index}`}>
								Unit
							</label>
							<input
								id={`edit-ingredient-unit-${recipe.id}-${index}`}
								type="text"
								value={ingredient.unit || ''}
								onChange={(event) =>
									handleIngredientChange(index, 'unit', event.target.value)
								}
							/>
						</div>
					</div>
				))}
			</fieldset>

      <button type="submit">Save changes</button>

			<button type="button" onClick={onCancel}>
				Cancel
			</button>
    </form>
  )
}

export default RecipeEditForm