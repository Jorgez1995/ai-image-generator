import streamlit as st
from utils.llm import analyze_prompt
from utils.image_gen import generate_image
from PIL import Image
import io

st.title("AI Image Generator")

st.write("Welcome! Let's build your custom image.")

# Step 1: User input
prompt = st.text_input("Enter your image idea:")

if st.button("Analyze Prompt"):
    if prompt:
        with st.spinner("Analyzing your prompt..."):
            suggestions = analyze_prompt(prompt)

            if suggestions:
                st.success("✅ Analysis complete!")

                # Store suggestions in session state
                st.session_state.suggestions = suggestions
                st.session_state.user_prompt = prompt
                # Clear previous selections
                st.session_state.final_prompt = None
            else:
                st.error("Failed to analyze prompt. Please try again.")
    else:
        st.warning("Please enter a prompt first!")

# Step 2: Display suggestions with custom option
if "suggestions" in st.session_state:
    st.divider()
    st.subheader("Choose options for your image:")

    suggestions = st.session_state.suggestions
    selections = {}

    # Display each category
    for category, options in suggestions.items():
        st.write(f"**{category.title()}:**")

        # Add "Write your own" option
        options_with_custom = options + ["✏️ Write your own"]

        selected = st.radio(
            f"Select {category}:", options_with_custom, key=f"radio_{category}"
        )

        # If user selects "Write your own", show text input
        if selected == "✏️ Write your own":
            custom_value = st.text_input(
                f"Enter custom {category}:",
                key=f"custom_{category}",
                placeholder=f"Type your custom {category} here...",
            )
            selections[category] = custom_value if custom_value else selected
        else:
            selections[category] = selected

    # Step 3: Build final prompt button
    st.divider()
    if st.button("Build Final Prompt"):
        # Check if any custom fields are empty
        has_empty_custom = any(v == "✏️ Write your own" for v in selections.values())

        if has_empty_custom:
            st.warning("Please fill in all custom fields or select a different option.")
        else:
            st.session_state.final_prompt = selections
            st.success("✅ Prompt built!")

# Step 4: Display final prompt JSON and generate image
if "final_prompt" in st.session_state and st.session_state.final_prompt:
    st.divider()
    st.subheader("Your Final Prompt:")
    st.json(st.session_state.final_prompt)

    # Generate image button
    if st.button("Generate Image"):
        with st.spinner("Generating your image... This may take 10-30 seconds."):
            image_bytes, gen_time = generate_image(st.session_state.final_prompt)

            if image_bytes:
                # Convert bytes to PIL Image for display
                image = Image.open(io.BytesIO(image_bytes))

                st.success(f"✅ Image generated in {gen_time:.2f} seconds!")
                st.image(
                    image, caption="Your Generated Image", use_container_width=True
                )

                # Optional: Download button
                st.download_button(
                    label="Download Image",
                    data=image_bytes,
                    file_name="generated_image.png",
                    mime="image/png",
                )
            else:
                st.error("Failed to generate image. Please try again.")
