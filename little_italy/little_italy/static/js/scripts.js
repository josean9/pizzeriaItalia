const pizzaData = JSON.parse('{{ pizzas_json|escapejs }}');

function showPizzaInfo(pizzaId, size) {
    const pizza = pizzaData.find(p => p.id == pizzaId);
    const details = document.getElementById(`details-${pizzaId}`);
    const priceSpan = document.getElementById(`price-${pizzaId}`);
    const ingredientsTable = document.getElementById(`ingredients-${pizzaId}`);

    if (size === 'small') {
        priceSpan.textContent = pizza.price_small;
        ingredientsTable.innerHTML = `
            <table>
                <thead>
                    <tr>
                        <th>Ingrediente</th>
                        <th>Calorías</th>
                        <th>Carbohidratos</th>
                        <th>Proteínas</th>
                        <th>Potasio</th>
                    </tr>
                </thead>
                <tbody>
                    ${pizza.ingredients_small.map(ing => `
                        <tr>
                            <td>${ing.name}</td>
                            <td>${ing.calories}</td>
                            <td>${ing.carbs || 'N/A'}</td>
                            <td>${ing.protein || 'N/A'}</td>
                            <td>${ing.potassium || 'N/A'} mg</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    } else if (size === 'medium') {
        priceSpan.textContent = pizza.price_medium;
        ingredientsTable.innerHTML = `
            <table>
                <thead>
                    <tr>
                        <th>Ingrediente</th>
                        <th>Calorías</th>
                        <th>Carbohidratos</th>
                        <th>Proteínas</th>
                        <th>Potasio</th>
                    </tr>
                </thead>
                <tbody>
                    ${pizza.ingredients_medium.map(ing => `
                        <tr>
                            <td>${ing.name}</td>
                            <td>${ing.calories}</td>
                            <td>${ing.carbs || 'N/A'}</td>
                            <td>${ing.protein || 'N/A'}</td>
                            <td>${ing.potassium || 'N/A'} mg</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    } else if (size === 'large') {
        priceSpan.textContent = pizza.price_large;
        ingredientsTable.innerHTML = `
            <table>
                <thead>
                    <tr>
                        <th>Ingrediente</th>
                        <th>Calorías</th>
                        <th>Carbohidratos</th>
                        <th>Proteínas</th>
                        <th>Potasio</th>
                    </tr>
                </thead>
                <tbody>
                    ${pizza.ingredients_large.map(ing => `
                        <tr>
                            <td>${ing.name}</td>
                            <td>${ing.calories}</td>
                            <td>${ing.carbs || 'N/A'}</td>
                            <td>${ing.protein || 'N/A'}</td>
                            <td>${ing.potassium || 'N/A'} mg</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    }

    details.style.display = 'block';
}


function hidePizzaInfo(pizzaId) {
    const details = document.getElementById(`details-${pizzaId}`);
    details.style.display = 'none';
}
