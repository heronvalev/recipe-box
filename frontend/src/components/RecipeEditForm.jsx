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

	function handleRemoveIngredient(indexToRemove) {
		if (ingredients.length <= 1) {
			return
		}

		const updatedIngredients = ingredients.filter((ingredient, ingredientIndex) => {
			return ingredientIndex !== indexToRemove
		})

		setIngredients(updatedIngredients)
	}

	async function handleSubmit(event) {
		event.preventDefault()

		const updatedRecipe = {
			title: title,
			instructions: instructions,
			ingredients: ingredients,
		}

		try {
			const response = await fetch(
				`http://127.0.0.1:8000/recipes/${recipe.id}`,
				{
					method: 'PUT',
					headers: {
					'Content-Type': 'application/json',
					},
					body: JSON.stringify(updatedRecipe),
				}
			)

			if (!response.ok) {
			throw new Error('Could not update recipe.')
			}

			onRecipeUpdated()
			onCancel()
		} catch (error) {
			console.error(error)
		}
	}

  return (
    <form onSubmit={handleSubmit}>
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
					<div key={index} className="ingredient-edit-card">

						<button
							type="button"
							className="remove-ingredient-button"
							onClick={() => handleRemoveIngredient(index)}
							disabled={ingredients.length <= 1}
							aria-label={`Remove ingredient ${index + 1}`}
						>
							×
						</button>

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
		
		<button type="button" onClick={handleAddIngredient}>
			Add another ingredient
		</button>	

      <button type="submit">Save changes</button>

			<button type="button" onClick={onCancel}>
				Cancel
			</button>
    </form>
  )
}

export default RecipeEditForm