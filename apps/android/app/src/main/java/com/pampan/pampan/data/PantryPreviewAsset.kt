package com.pampan.pampan.data

import android.content.Context
import com.pampan.pampan.domain.PantryCategory
import com.pampan.pampan.domain.PantryContract
import com.pampan.pampan.domain.PantryItem
import com.pampan.pampan.domain.PantrySnapshot
import org.json.JSONArray
import org.json.JSONObject

object PantryPreviewAsset {
    private const val ASSET_NAME = "pantry-contract-v1.sample.json"
    private val rootKeys = setOf("contractVersion", "categories", "items")
    private val categoryKeys = setOf("id", "name")
    private val itemKeys =
        setOf("id", "name", "quantity", "unit", "expiryDate", "categoryId")

    fun load(context: Context): PantrySnapshot {
        val document =
            context.assets
                .open(ASSET_NAME)
                .bufferedReader()
                .use { reader -> JSONObject(reader.readText()) }
        requireExactKeys(document, rootKeys, "root")
        require(requireString(document, "contractVersion", "root") == PantryContract.VERSION) {
            "Unsupported pantry contract version."
        }

        val categories =
            document.getJSONArray("categories").mapObjects("categories") { value, location ->
                requireExactKeys(value, categoryKeys, location)
                PantryCategory(
                    id = requireString(value, "id", location),
                    name = requireString(value, "name", location),
                )
            }
        val items =
            document.getJSONArray("items").mapObjects("items") { value, location ->
                requireExactKeys(value, itemKeys, location)
                PantryItem(
                    id = requireString(value, "id", location),
                    name = requireString(value, "name", location),
                    quantity =
                        PantryContract.parseQuantity(
                            requireString(value, "quantity", location),
                        ),
                    unit = requireString(value, "unit", location),
                    expiryDate =
                        PantryContract.parseExpiryDate(
                            requireString(value, "expiryDate", location),
                        ),
                    categoryId = requireString(value, "categoryId", location),
                )
            }
        return PantrySnapshot(categories = categories, items = items)
    }

    private fun requireExactKeys(
        value: JSONObject,
        expected: Set<String>,
        location: String,
    ) {
        val actual = value.keys().asSequence().toSet()
        require(actual == expected) {
            "$location fields must match pantry contract v1 exactly."
        }
    }

    private fun requireString(
        value: JSONObject,
        key: String,
        location: String,
    ): String {
        val field = value.get(key)
        require(field is String) {
            "$location.$key must be a string."
        }
        return field
    }

    private fun <T> JSONArray.mapObjects(
        name: String,
        transform: (JSONObject, String) -> T,
    ): List<T> =
        List(length()) { index ->
            transform(getJSONObject(index), "$name[$index]")
        }
}
