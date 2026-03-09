# Simplified Adaptive Lighting

This *blueprint* for Home Assistant is inspired by the [Adaptive Lighting integration](https://github.com/basnijholt/adaptive-lighting) and automatically adjusts connected lights throughout the day and even at night. Compared to the integration, it is much simpler and offers far fewer options.

It is available in these languages : 

- [French](README.fr.md)
- [German](README.de.md)

## Using the Blueprint

You can add this *blueprint* to your Home Assistant instance using this direct link:

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fnicolinuxfr%2Fsimple-adaptive-lighting-blueprint%2Fgh-pages%2Fen%2Fadaptive_lighting.yaml)

Alternatively, you can copy this link to paste into Home Assistant when adding a blueprint:

	https://raw.githubusercontent.com/nicolinuxfr/simple-adaptive-lighting-blueprint/gh-pages/en/adaptive_lighting.yaml

## Configuration

The automation created from the blueprint only requires one parameter: one or more lights. You can enter multiple different entities or a Home Assistant group. The other parameters can be left at their default configuration or adjusted to your needs.

Here is the list of options with some explanations where needed:

- **Main settings**: choose the minimum and maximum brightness, as well as the minimum and maximum white temperature for the lights.
- **Entity control**: by selecting a boolean entity (of type `input_boolean` or `binary_sensor`), you can add control over the automation without disabling it. The entity must be active for the automation to adjust the lights, and when it is disabled, the lights stay at the last automatic setting. If you enable the automatic deactivation on color option, member lights inside a selected Home Assistant group are also monitored individually.
- **Weather**: by selecting a weather entity, the automation's behavior is modified based on weather conditions. The idea is to slightly vary the parameters to have dimmer and warmer lighting when weather conditions are bad.
- **Night mode**: by selecting a boolean entity (of type `input_boolean` or `binary_sensor`), you can set up specific fixed lighting for the night. When the entity is active, automatic adjustments are disabled and the brightness and color temperature settings are used instead. This allows daytime settings bright enough to be comfortable, while keeping nighttime lighting much dimmer.

For all three optional features (entity control, weather and night mode), leaving the field empty disables the feature entirely.

## How It Works

The automation activates as soon as the selected lights turn on. From there, it triggers every five minutes to adjust the brightness and white temperature based on the defined parameters, the time of day, and the automatically calculated curve. Each transition is spread over ten seconds to avoid visible changes. To limit issues with certain lights, the automation adopts a two-step strategy and alternates between brightness and white temperature at each update.

If a control entity is used, adaptation automatically stops as soon as the entity is disabled and resumes if it is re-enabled. In this case, there is no delay — the correct values are immediately sent, with a smooth progression over 10 seconds. With automatic deactivation on color enabled, the blueprint also watches the individual lights contained in any selected Home Assistant group.

If weather adaptation is enabled, the curve is slightly adjusted based on current weather conditions. This information is only updated when the lights are initially turned on, to save resources.

Several strategies are in place to slightly adjust the automation's behavior depending on the situation. For example, the curve is different when only one light is configured compared to an automation controlling multiple lights.

## Limitations

This blueprint intentionally does not handle certain features:

- No color management, only white temperature;
- No curve adjustment — the retained parameters are those that suit my needs;
- No adjustments possible for start and end times — only sunrise and sunset times at your home's location are used;
- No manual light control in case of individual changes — the automation will always trigger every five minutes and overwrite changes;
- Certainly many others.

## Disclaimer

I did not directly code this *blueprint* myself — I used tools like Codex and Claude Code to create it. It is therefore offered without warranty, except that it works perfectly for me. I have tested it with multiple configurations and many lights and have noted no issues.

The translations are also generated automatically by these tools — I wrote all the text in French.

## Contributing

All contributions are welcome, to fix bugs or add features. However, I want to keep the configuration as simple as possible — my intention is not to reproduce the Adaptive Lighting integration.
