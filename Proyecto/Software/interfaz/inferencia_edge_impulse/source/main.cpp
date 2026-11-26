#include <algorithm>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#include "edge-impulse-sdk/classifier/ei_run_classifier.h"

static std::vector<float> features;

static int get_signal_data(size_t offset, size_t length, float *out_ptr) {
    std::copy(
        features.begin() + offset,
        features.begin() + offset + length,
        out_ptr
    );
    return EIDSP_OK;
}

static bool load_features(const char *path) {
    std::ifstream input(path, std::ios::binary);

    if (!input) {
        return false;
    }

    std::ostringstream buffer;
    buffer << input.rdbuf();
    std::string text = buffer.str();

    for (char &character : text) {
        if (
            character == ',' ||
            character == ';' ||
            character == '\t' ||
            character == '\r' ||
            character == '\n'
        ) {
            character = ' ';
        }
    }

    std::istringstream values(text);
    float value;

    while (values >> value) {
        features.push_back(value);
    }

    return true;
}

int main(int argc, char **argv) {
    if (argc != 2) {
        std::cerr << "Uso: app.exe <archivo_con_muestras>\n";
        return 2;
    }

    if (!load_features(argv[1])) {
        std::cerr << "No se pudo abrir el archivo de muestras.\n";
        return 3;
    }

    if (features.size() != EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE) {
        std::cerr
            << "Cantidad de muestras incorrecta. Esperadas: "
            << EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE
            << ", recibidas: "
            << features.size()
            << "\n";

        return 4;
    }

    signal_t signal;
    signal.total_length = features.size();
    signal.get_data = &get_signal_data;

    ei_impulse_result_t result = {};

    run_classifier_init();

    EI_IMPULSE_ERROR error =
        run_classifier(&signal, &result, false);

    if (error != EI_IMPULSE_OK) {
        std::cerr
            << "Edge Impulse devolvio el error: "
            << error
            << "\n";

        return 5;
    }

    size_t best_index = 0;

    for (
        size_t index = 1;
        index < EI_CLASSIFIER_LABEL_COUNT;
        index++
    ) {
        if (
            result.classification[index].value >
            result.classification[best_index].value
        ) {
            best_index = index;
        }
    }

    std::cout << std::fixed << std::setprecision(6);

    std::cout
        << "{\"label\":\""
        << result.classification[best_index].label
        << "\",\"confidence\":"
        << result.classification[best_index].value
        << ",\"predictions\":{";

    for (
        size_t index = 0;
        index < EI_CLASSIFIER_LABEL_COUNT;
        index++
    ) {
        if (index > 0) {
            std::cout << ',';
        }

        std::cout
            << '"'
            << result.classification[index].label
            << "\":"
            << result.classification[index].value;
    }

    std::cout << "}}\n";

    return 0;
}