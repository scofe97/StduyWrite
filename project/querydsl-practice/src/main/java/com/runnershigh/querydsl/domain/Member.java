package com.runnershigh.querydsl.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Embedded;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import lombok.AccessLevel;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Member {

    @Id
    @GeneratedValue
    @Column(name = "member_id")
    private Long id;

    @Column(nullable = false, length = 50)
    private String username;

    @Column(length = 100)
    private String email;

    private int age;

    @Embedded
    private Address address;

    @Builder
    private Member(String username, String email, int age, Address address) {
        this.username = username;
        this.email = email;
        this.age = age;
        this.address = address;
    }

    public void changeAge(int age) {
        this.age = age;
    }
}
