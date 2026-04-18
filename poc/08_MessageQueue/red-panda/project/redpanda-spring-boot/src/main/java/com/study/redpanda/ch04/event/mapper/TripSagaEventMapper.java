package com.study.redpanda.ch04.event.mapper;

import com.study.redpanda.avro.trip.TripBookFlightCommand;
import com.study.redpanda.avro.trip.TripBookHotelCommand;
import com.study.redpanda.avro.trip.TripCancelFlightCommand;
import com.study.redpanda.avro.trip.TripFlightBooked;
import com.study.redpanda.avro.trip.TripFlightBookingFailed;
import com.study.redpanda.avro.trip.TripFlightCancelled;
import com.study.redpanda.avro.trip.TripHotelBooked;
import com.study.redpanda.avro.trip.TripHotelBookingFailed;
import com.study.redpanda.ch04.command.BookFlightCommand;
import com.study.redpanda.ch04.command.BookHotelCommand;
import com.study.redpanda.ch04.command.CancelFlightCommand;
import com.study.redpanda.ch04.event.FlightBooked;
import com.study.redpanda.ch04.event.FlightBookingFailed;
import com.study.redpanda.ch04.event.FlightCancelled;
import com.study.redpanda.ch04.event.HotelBooked;
import com.study.redpanda.ch04.event.HotelBookingFailed;

import java.time.Instant;
import java.time.LocalDate;

/**
 * 도메인 레코드 ↔ Avro 생성 클래스 변환 매퍼
 *
 * - toAvro(): 도메인 레코드 → Avro SpecificRecord (Kafka 전송용)
 * - toDomain(): Avro SpecificRecord → 도메인 레코드 (비즈니스 로직용)
 *
 * Instant ↔ String: Instant.toString() / Instant.parse()
 * LocalDate ↔ String: LocalDate.toString() / LocalDate.parse()
 * CharSequence → String: .toString()
 */
public class TripSagaEventMapper {

    private TripSagaEventMapper() {}

    // ─── BookFlightCommand ───────────────────────────────────────────────────

    public static TripBookFlightCommand toAvro(BookFlightCommand cmd) {
        return TripBookFlightCommand.newBuilder()
                .setTripId(cmd.tripId())
                .setSagaId(cmd.sagaId())
                .setDeparture(cmd.departure())
                .setArrival(cmd.arrival())
                .setTravelDate(cmd.travelDate().toString())
                .build();
    }

    public static BookFlightCommand toDomain(TripBookFlightCommand avro) {
        return new BookFlightCommand(
                avro.getTripId().toString(),
                avro.getSagaId().toString(),
                avro.getDeparture().toString(),
                avro.getArrival().toString(),
                LocalDate.parse(avro.getTravelDate()));
    }

    // ─── CancelFlightCommand ─────────────────────────────────────────────────

    public static TripCancelFlightCommand toAvro(CancelFlightCommand cmd) {
        return TripCancelFlightCommand.newBuilder()
                .setTripId(cmd.tripId())
                .setSagaId(cmd.sagaId())
                .setReservationId(cmd.reservationId())
                .build();
    }

    public static CancelFlightCommand toDomain(TripCancelFlightCommand avro) {
        return new CancelFlightCommand(
                avro.getTripId().toString(),
                avro.getSagaId().toString(),
                avro.getReservationId().toString());
    }

    // ─── BookHotelCommand ────────────────────────────────────────────────────

    public static TripBookHotelCommand toAvro(BookHotelCommand cmd) {
        return TripBookHotelCommand.newBuilder()
                .setTripId(cmd.tripId())
                .setSagaId(cmd.sagaId())
                .setHotelName(cmd.hotelName())
                .setCheckIn(cmd.checkIn().toString())
                .setCheckOut(cmd.checkOut().toString())
                .build();
    }

    public static BookHotelCommand toDomain(TripBookHotelCommand avro) {
        return new BookHotelCommand(
                avro.getTripId().toString(),
                avro.getSagaId().toString(),
                avro.getHotelName().toString(),
                LocalDate.parse(avro.getCheckIn()),
                LocalDate.parse(avro.getCheckOut()));
    }

    // ─── FlightBooked ────────────────────────────────────────────────────────

    public static TripFlightBooked toAvro(FlightBooked event) {
        return TripFlightBooked.newBuilder()
                .setTripId(event.tripId())
                .setSagaId(event.sagaId())
                .setTimestamp(event.timestamp().toString())
                .setReservationId(event.reservationId())
                .build();
    }

    public static FlightBooked toDomain(TripFlightBooked avro) {
        return new FlightBooked(
                avro.getTripId().toString(),
                avro.getSagaId().toString(),
                Instant.parse(avro.getTimestamp()),
                avro.getReservationId().toString());
    }

    // ─── FlightBookingFailed ─────────────────────────────────────────────────

    public static TripFlightBookingFailed toAvro(FlightBookingFailed event) {
        return TripFlightBookingFailed.newBuilder()
                .setTripId(event.tripId())
                .setSagaId(event.sagaId())
                .setTimestamp(event.timestamp().toString())
                .setReason(event.reason())
                .build();
    }

    public static FlightBookingFailed toDomain(TripFlightBookingFailed avro) {
        return new FlightBookingFailed(
                avro.getTripId().toString(),
                avro.getSagaId().toString(),
                Instant.parse(avro.getTimestamp()),
                avro.getReason().toString());
    }

    // ─── FlightCancelled ─────────────────────────────────────────────────────

    public static TripFlightCancelled toAvro(FlightCancelled event) {
        return TripFlightCancelled.newBuilder()
                .setTripId(event.tripId())
                .setSagaId(event.sagaId())
                .setTimestamp(event.timestamp().toString())
                .setReservationId(event.reservationId())
                .build();
    }

    public static FlightCancelled toDomain(TripFlightCancelled avro) {
        return new FlightCancelled(
                avro.getTripId().toString(),
                avro.getSagaId().toString(),
                Instant.parse(avro.getTimestamp()),
                avro.getReservationId().toString());
    }

    // ─── HotelBooked ─────────────────────────────────────────────────────────

    public static TripHotelBooked toAvro(HotelBooked event) {
        return TripHotelBooked.newBuilder()
                .setTripId(event.tripId())
                .setSagaId(event.sagaId())
                .setTimestamp(event.timestamp().toString())
                .setReservationId(event.reservationId())
                .build();
    }

    public static HotelBooked toDomain(TripHotelBooked avro) {
        return new HotelBooked(
                avro.getTripId().toString(),
                avro.getSagaId().toString(),
                Instant.parse(avro.getTimestamp()),
                avro.getReservationId().toString());
    }

    // ─── HotelBookingFailed ──────────────────────────────────────────────────

    public static TripHotelBookingFailed toAvro(HotelBookingFailed event) {
        return TripHotelBookingFailed.newBuilder()
                .setTripId(event.tripId())
                .setSagaId(event.sagaId())
                .setTimestamp(event.timestamp().toString())
                .setReason(event.reason())
                .build();
    }

    public static HotelBookingFailed toDomain(TripHotelBookingFailed avro) {
        return new HotelBookingFailed(
                avro.getTripId().toString(),
                avro.getSagaId().toString(),
                Instant.parse(avro.getTimestamp()),
                avro.getReason().toString());
    }
}
