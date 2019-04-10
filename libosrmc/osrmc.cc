/*

The MIT License (MIT)

Copyright (c) 2016 Daniel J. Hofmann

Copyright (c) 2018 Cayetano Benavent - Geographica

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

*/

#include <cassert>
#include <cmath>
#include <utility>
#include <string>
#include <stdexcept>
#include <iostream>
#include <fstream>

#include <osrm/coordinate.hpp>
#include <osrm/engine_config.hpp>
#include <osrm/json_container.hpp>
#include <osrm/osrm.hpp>
#include <osrm/route_parameters.hpp>
#include <osrm/table_parameters.hpp>
#include <osrm/nearest_parameters.hpp>
#include <osrm/match_parameters.hpp>
#include <osrm/status.hpp>
#include <osrm/storage_config.hpp>

#include "osrmc.h"

/** ABI stability **/

unsigned osrmc_get_version(void) { return OSRMC_VERSION; }

int osrmc_is_abi_compatible(void) { return osrmc_get_version() >> 16u == OSRMC_VERSION_MAJOR; }

/** API **/

/* Error handling */

struct osrmc_error final {
  std::string message;
};

const char* osrmc_error_message(osrmc_error_t error) { return error->message.c_str(); }

void osrmc_error_destruct(osrmc_error_t error) { delete error; }


/* Config and osrmc */

osrmc_config_t osrmc_config_construct(const char* base_path, const bool contraction, osrmc_error_t* error) try {
  auto* out = new osrm::EngineConfig;

  if (base_path)
  {
      out->storage_config = osrm::StorageConfig(base_path);
      out->use_shared_memory = false;
  }
  else
  {
      out->use_shared_memory = true;
  }

  if (contraction)
  {
      out->algorithm = osrm::EngineConfig::Algorithm::CH;
  }
  else
  {
      out->algorithm = osrm::EngineConfig::Algorithm::MLD;
  }

  return reinterpret_cast<osrmc_config_t>(out);
} catch (const std::exception& e) {
  *error = new osrmc_error{e.what()};
  return nullptr;
}

void osrmc_config_destruct(osrmc_config_t config) { delete reinterpret_cast<osrm::EngineConfig*>(config); }

osrmc_osrm_t osrmc_osrm_construct(osrmc_config_t config, osrmc_error_t* error) try {
  auto* config_typed = reinterpret_cast<osrm::EngineConfig*>(config);
  auto* out = new osrm::OSRM(*config_typed);

  return reinterpret_cast<osrmc_osrm_t>(out);
} catch (const std::exception& e) {
  *error = new osrmc_error{e.what()};
  return nullptr;
}

void osrmc_osrm_destruct(osrmc_osrm_t osrm) { delete reinterpret_cast<osrm::OSRM*>(osrm); }


/* Generic parameters */

void osrmc_params_add_coordinate(osrmc_params_t params, float longitude, float latitude, osrmc_error_t* error) try {
  auto* params_typed = reinterpret_cast<osrm::engine::api::BaseParameters*>(params);

  auto longitude_typed = osrm::util::FloatLongitude{longitude};
  auto latitude_typed = osrm::util::FloatLatitude{latitude};

  params_typed->coordinates.emplace_back(std::move(longitude_typed), std::move(latitude_typed));
} catch (const std::exception& e) {
  *error = new osrmc_error{e.what()};
}

void osrmc_params_add_coordinate_with(osrmc_params_t params, float longitude, float latitude, float radius, int bearing,
                                      int range, osrmc_error_t* error) try {
  auto* params_typed = reinterpret_cast<osrm::engine::api::BaseParameters*>(params);

  auto longitude_typed = osrm::util::FloatLongitude{longitude};
  auto latitude_typed = osrm::util::FloatLatitude{latitude};

  osrm::engine::Bearing bearing_typed{static_cast<short>(bearing), static_cast<short>(range)};

  params_typed->coordinates.emplace_back(std::move(longitude_typed), std::move(latitude_typed));
  params_typed->radiuses.emplace_back(radius);
  params_typed->bearings.emplace_back(std::move(bearing_typed));
} catch (const std::exception& e) {
  *error = new osrmc_error{e.what()};
}

void osrmc_params_exclude(osrmc_params_t params, const char* excluded_class, osrmc_error_t* error) try {
  auto* params_typed = reinterpret_cast<osrm::engine::api::BaseParameters*>(params);

  params_typed->exclude.emplace_back(std::move(excluded_class));
} catch (const std::exception& e) {
  *error = new osrmc_error{e.what()};
}

/* Route service */

osrmc_route_params_t osrmc_route_params_construct(osrmc_error_t* error) try {
  auto* out = new osrm::RouteParameters;
  out->geometries = osrm::RouteParameters::GeometriesType::Polyline;

  return reinterpret_cast<osrmc_route_params_t>(out);
} catch (const std::exception& e) {
  *error = new osrmc_error{e.what()};
  return nullptr;
}

void osrmc_route_params_destruct(osrmc_route_params_t params) {
  delete reinterpret_cast<osrm::RouteParameters*>(params);
}

void osrmc_route_params_add_steps(osrmc_route_params_t params, int on) {
  auto* params_typed = reinterpret_cast<osrm::RouteParameters*>(params);
  params_typed->steps = on;
}

void osrmc_route_params_add_continue_straight(osrmc_route_params_t params, int on) {
  auto* params_typed = reinterpret_cast<osrm::RouteParameters*>(params);
  params_typed->continue_straight = on;
}

void osrmc_route_params_add_overview_full(osrmc_route_params_t params, int on) {
  auto* params_typed = reinterpret_cast<osrm::RouteParameters*>(params);

  if (on)
  {
    params_typed->overview = osrm::RouteParameters::OverviewType::Full;
  }
  else
  {
    params_typed->overview = osrm::RouteParameters::OverviewType::Simplified;
  }
}

void osrmc_route_params_add_alternatives(osrmc_route_params_t params, int on) {
  auto* params_typed = reinterpret_cast<osrm::RouteParameters*>(params);
  params_typed->alternatives = on;
}

osrmc_route_response_t osrmc_route(osrmc_osrm_t osrm, osrmc_route_params_t params, osrmc_error_t* error) try {
  auto* osrm_typed = reinterpret_cast<osrm::OSRM*>(osrm);
  auto* params_typed = reinterpret_cast<osrm::RouteParameters*>(params);

  auto* out = new osrm::json::Object;
  const auto status = osrm_typed->Route(*params_typed, *out);

  if (status == osrm::Status::Ok)
    return reinterpret_cast<osrmc_route_response_t>(out);

  *error = new osrmc_error{"service request failed"};
  return nullptr;
} catch (const std::exception& e) {
  *error = new osrmc_error{e.what()};
  return nullptr;
}

void osrmc_route_with(osrmc_osrm_t osrm, osrmc_route_params_t params, osrmc_waypoint_handler_t handler, void* data,
                      osrmc_error_t* error) try {
  auto* osrm_typed = reinterpret_cast<osrm::OSRM*>(osrm);
  auto* params_typed = reinterpret_cast<osrm::RouteParameters*>(params);

  osrm::json::Object result;
  const auto status = osrm_typed->Route(*params_typed, result);

  if (status != osrm::Status::Ok) {
    *error = new osrmc_error{"service request failed"};
    return;
  }

  const auto& waypoints = result.values.at("waypoints").get<osrm::json::Array>().values;

  for (const auto& waypoint : waypoints) {
    const auto& waypoint_typed = waypoint.get<osrm::json::Object>();
    const auto& location = waypoint_typed.values.at("location").get<osrm::json::Array>().values;

    const auto& name = waypoint_typed.values.at("name").get<osrm::json::String>().value;
    const auto longitude = location[0].get<osrm::json::Number>().value;
    const auto latitude = location[1].get<osrm::json::Number>().value;

    (void)handler(data, name.c_str(), longitude, latitude);
  }
} catch (const std::exception& e) {
  *error = new osrmc_error{e.what()};
}

void osrmc_route_response_destruct(osrmc_route_response_t response) {
  delete reinterpret_cast<osrm::json::Object*>(response);
}

float osrmc_route_response_distance(osrmc_route_response_t response, osrmc_error_t* error) try {
  auto* response_typed = reinterpret_cast<osrm::json::Object*>(response);

  auto& routes = response_typed->values["routes"].get<osrm::json::Array>();
  auto& route = routes.values.at(0).get<osrm::json::Object>();

  const auto distance = route.values["distance"].get<osrm::json::Number>().value;
  return distance;
} catch (const std::exception& e) {
  *error = new osrmc_error{e.what()};
  return INFINITY;
}

float osrmc_route_response_duration(osrmc_route_response_t response, osrmc_error_t* error) try {
  auto* response_typed = reinterpret_cast<osrm::json::Object*>(response);

  auto& routes = response_typed->values["routes"].get<osrm::json::Array>();
  auto& route = routes.values.at(0).get<osrm::json::Object>();

  const auto duration = route.values["duration"].get<osrm::json::Number>().value;
  return duration;
} catch (const std::exception& e) {
  *error = new osrmc_error{e.what()};
  return INFINITY;
}

const char* osrmc_route_response_geometry(osrmc_route_response_t response, osrmc_error_t* error) try {
  auto* response_typed = reinterpret_cast<osrm::json::Object*>(response);
  auto& routes = response_typed->values["routes"].get<osrm::json::Array>();
  auto& route = routes.values.at(0).get<osrm::json::Object>();
  const auto geometry = route.values["geometry"].get<osrm::json::String>().value;

  char* geom_out = new char [geometry.length() + 1];
  strcpy(geom_out, geometry.c_str());
  return geom_out;
} catch (const std::exception& e) {
  *error = new osrmc_error{e.what()};
  return nullptr;
}

void osrmc_route_response_geometry_legs(osrmc_route_response_t response, const char* base_path, osrmc_error_t* error) try {
  auto* response_typed = reinterpret_cast<osrm::json::Object*>(response);
  auto& routes = response_typed->values["routes"].get<osrm::json::Array>();
  auto& route = routes.values.at(0).get<osrm::json::Object>();
  const auto geometry = route.values["geometry"].get<osrm::json::String>().value;
  const auto &legs = route.values["legs"].get<osrm::json::Array>().values;

  std::ofstream pFile;
  pFile.open(base_path);

  for (const auto &leg : legs)
  {
      const auto &leg_object = leg.get<osrm::json::Object>();
      const auto &steps = leg_object.values.at("steps").get<osrm::json::Array>().values;

      int step_ct = 0;

      for (const auto &step : steps)
      {
          const auto &step_object = step.get<osrm::json::Object>();
          const auto step_dist = step_object.values.at("distance").get<osrm::json::Number>().value;
          const auto step_dur = step_object.values.at("duration").get<osrm::json::Number>().value;
          const auto step_geom = step_object.values.at("geometry").get<osrm::json::String>().value;

          pFile << step_ct << "," << step_dist << "," << step_dur << "," << step_geom << std::endl;

          ++step_ct;
      }
  }
  pFile.close();

} catch (const std::exception& e) {
  *error = new osrmc_error{e.what()};
}


/* Table service */

osrmc_table_params_t osrmc_table_params_construct(osrmc_error_t* error) try {
  auto* out = new osrm::TableParameters;
  out->annotations = osrm::TableParameters::AnnotationsType::All;
  return reinterpret_cast<osrmc_table_params_t>(out);
} catch (const std::exception& e) {
  *error = new osrmc_error{e.what()};
  return nullptr;
}

void osrmc_table_params_destruct(osrmc_table_params_t params) {
  delete reinterpret_cast<osrm::TableParameters*>(params);
}

void osrmc_table_params_add_source(osrmc_table_params_t params, size_t index, osrmc_error_t* error) try {
  auto* params_typed = reinterpret_cast<osrm::TableParameters*>(params);
  params_typed->sources.emplace_back(index);
} catch (const std::exception& e) {
  *error = new osrmc_error{e.what()};
}

void osrmc_table_params_add_destination(osrmc_table_params_t params, size_t index, osrmc_error_t* error) try {
  auto* params_typed = reinterpret_cast<osrm::TableParameters*>(params);
  params_typed->destinations.emplace_back(index);
} catch (const std::exception& e) {
  *error = new osrmc_error{e.what()};
}

osrmc_table_response_t osrmc_table(osrmc_osrm_t osrm, osrmc_table_params_t params, osrmc_error_t* error) try {
  auto* osrm_typed = reinterpret_cast<osrm::OSRM*>(osrm);
  auto* params_typed = reinterpret_cast<osrm::TableParameters*>(params);

  auto* out = new osrm::json::Object;
  const auto status = osrm_typed->Table(*params_typed, *out);

  if (status == osrm::Status::Ok)
    return reinterpret_cast<osrmc_table_response_t>(out);

  *error = new osrmc_error{"service request failed"};
  return nullptr;
} catch (const std::exception& e) {
  *error = new osrmc_error{e.what()};
  return nullptr;
}

void osrmc_table_response_destruct(osrmc_table_response_t response) {
  delete reinterpret_cast<osrm::json::Object*>(response);
}

float osrmc_table_response_duration(osrmc_table_response_t response, unsigned long from, unsigned long to,
                                    osrmc_error_t* error) try {
  auto* response_typed = reinterpret_cast<osrm::json::Object*>(response);

  auto& durations = response_typed->values["durations"].get<osrm::json::Array>();
  auto& durations_from_to_all = durations.values.at(from).get<osrm::json::Array>();
  auto duration = durations_from_to_all.values.at(to).get<osrm::json::Number>().value;

  return duration;
} catch (const std::exception& e) {
  *error = new osrmc_error{e.what()};
  return INFINITY;
}

float osrmc_table_response_distance(osrmc_table_response_t response, unsigned long from, unsigned long to,
                                    osrmc_error_t* error) try {
  auto* response_typed = reinterpret_cast<osrm::json::Object*>(response);

  auto& distances = response_typed->values["distances"].get<osrm::json::Array>();
  auto& distances_from_to_all = distances.values.at(from).get<osrm::json::Array>();
  auto distance = distances_from_to_all.values.at(to).get<osrm::json::Number>().value;

  return distance;
} catch (const std::exception& e) {
  *error = new osrmc_error{e.what()};
  return INFINITY;
}


/* Nearest service */

osrmc_nearest_params_t osrmc_nearest_params_construct(osrmc_error_t* error) try {
  auto* out = new osrm::NearestParameters;
  return reinterpret_cast<osrmc_nearest_params_t>(out);
} catch (const std::exception& e) {
  *error = new osrmc_error{e.what()};
  return nullptr;
}

void osrmc_nearest_params_destruct(osrmc_nearest_params_t params) {
  delete reinterpret_cast<osrm::NearestParameters*>(params);
}

osrmc_nearest_response_t osrmc_nearest(osrmc_osrm_t osrm, osrmc_nearest_params_t params,
                                       osrmc_error_t* error) try {
  auto* osrm_typed = reinterpret_cast<osrm::OSRM*>(osrm);
  auto* params_typed = reinterpret_cast<osrm::NearestParameters*>(params);

  auto* out = new osrm::json::Object;
  const auto status = osrm_typed->Nearest(*params_typed, *out);

  if (status == osrm::Status::Ok)
    return reinterpret_cast<osrmc_nearest_response_t>(out);

  *error = new osrmc_error{"service request failed"};
  return nullptr;
} catch (const std::exception& e) {
  *error = new osrmc_error{e.what()};
  return nullptr;
}

void osrmc_nearest_response_destruct(osrmc_nearest_response_t response) {
  delete reinterpret_cast<osrm::json::Object*>(response);
}

void osrmc_nearest_set_number_of_results(osrmc_nearest_params_t params, unsigned n) {
  auto* params_typed = reinterpret_cast<osrm::NearestParameters*>(params);
  params_typed->number_of_results = n;
}

void osrmc_nearest_response_coordinates(osrmc_nearest_response_t response, float* coords, osrmc_error_t* error) try {
  auto* response_typed = reinterpret_cast<osrm::json::Object*>(response);

  const auto& waypoints = response_typed->values["waypoints"].get<osrm::json::Array>().values;

  for (const auto& waypoint : waypoints) {
    const auto& waypoint_typed = waypoint.get<osrm::json::Object>();
    const auto& location = waypoint_typed.values.at("location").get<osrm::json::Array>().values;

    const auto longitude = location[0].get<osrm::json::Number>().value;
    const auto latitude = location[1].get<osrm::json::Number>().value;

    coords[0] = latitude;
    coords[1] = longitude;
  }
} catch (const std::exception& e) {
  *error = new osrmc_error{e.what()};
}


/* Match service */

osrmc_match_params_t osrmc_match_params_construct(osrmc_error_t* error) try {
  auto* out = new osrm::MatchParameters;
  return reinterpret_cast<osrmc_match_params_t>(out);
} catch (const std::exception& e) {
  *error = new osrmc_error{e.what()};
  return nullptr;
}

void osrmc_match_params_destruct(osrmc_match_params_t params) {
  delete reinterpret_cast<osrm::MatchParameters*>(params);
}

void osrmc_match_params_add_timestamp(osrmc_match_params_t params, unsigned timestamp, osrmc_error_t* error) try {
  auto* params_typed = reinterpret_cast<osrm::MatchParameters*>(params);
  params_typed->timestamps.emplace_back(timestamp);
} catch (const std::exception& e) {
  *error = new osrmc_error{e.what()};
}
