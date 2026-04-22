// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CertificateStore {

    mapping(string => bool) public certificates;

    function addCertificate(string memory certHash) public {
        certificates[certHash] = true;
    }

    function verifyCertificate(string memory certHash) public view returns (bool) {
        return certificates[certHash];
    }
}